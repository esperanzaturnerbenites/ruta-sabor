import pandas as pd

from sentence_transformers import SentenceTransformer, util
from math import radians, sin, cos, sqrt, atan2

from app.models.place_filters import PlaceFilter
from app.models.place import Place, Geolocation

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def get_all_places(filters: PlaceFilter) -> list[Place]:
    url = "https://raw.githubusercontent.com/esperanzaturnerbenites/Places/refs/heads/main/Places.csv"
    df = pd.read_csv(url)

    cols_optional = ["ACTIVIDAD", "NOM-PROP", "BARRIO-COMERCIAL", "TEL-COM-1", "EMAIL-COMERCIAL"]
    for col in cols_optional:
        df[col] = df[col].astype(str).str.strip().replace("nan", None)

    df["BARRIO-COMERCIAL"] = df["BARRIO-COMERCIAL"].astype(str).str.strip().replace("nan", None)
    df["TEL-COM-1"] = df["TEL-COM-1"].astype(str).str.strip().replace("nan", None)

    df[['lat', 'lng']] = df['GEOLOCALIZACION'].str.extract(r'([-\d.]+),\s*([-\d.]+)')
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lng'] = pd.to_numeric(df['lng'], errors='coerce')

    if filters.search_mode == "chat" and filters.message:
        try:
            user_message = filters.message
            activities = df['ACTIVIDAD'].astype(str).tolist()
            activity_embeddings = model.encode(activities, convert_to_tensor=True)
            message_embedding = model.encode(user_message, convert_to_tensor=True)

            cosine_scores = util.cos_sim(message_embedding, activity_embeddings)[0].cpu().numpy()
            df["similarity"] = cosine_scores

            # Verifica si hay alguna actividad que realmente se parezca
            best_score = df["similarity"].max()
            print("🧠 Mejor coincidencia IA:", best_score)

            if best_score < 0.4:
                print("🤖 No se entendió bien la intención del usuario, muy diferente a comida.")
                return []  # Devuelve vacío, el frontend puede sugerir otra cosa

            # Si sí hay algo que se parece, lo filtramos
            df = df[df["similarity"] >= 0.5]

        except Exception as e:
            print("⚠️ Error en interpretación del mensaje:", e)
            return []

    # Si hay filtro por type_food, usamos IA para filtrar por similitud semántica
    if filters.type_food:
        try:
            activities = df['ACTIVIDAD'].astype(str).tolist()
            activity_embeddings = model.encode(activities, convert_to_tensor=True)
            query_embedding = model.encode(filters.type_food, convert_to_tensor=True)

            cosine_scores = util.cos_sim(query_embedding, activity_embeddings)[0].cpu().numpy()

            # Añadir columna de similitud al DataFrame
            df["similarity"] = cosine_scores

            # Filtrar los más similares
            df = df[df["similarity"] > 0.5]
        except Exception as e:
            print("Error en el filtrado por IA:", e)

    places = []
    for _, row in df.iterrows():
        try:
            if pd.isna(row["lat"]) or pd.isna(row["lng"]):
                continue

            place = Place(
                place_name=row["RAZON SOCIAL"],
                owner_name=row["NOM-PROP"],
                address=row["DIR-COMERCIAL"],
                neighborhood=row.get("BARRIO-COMERCIAL"),
                geolocation=Geolocation(lat=row["lat"], lng=row["lng"]),
                phone=row.get("TEL-COM-1"),
                email=row.get("EMAIL-COMERCIAL"),
                activity=row["ACTIVIDAD"]
            )

            places.append(place)
        except Exception as e:
            print(f"Error en fila {row.to_dict()} → {e}")

    if filters.coords:
        try:
            lat_user, lng_user = map(float, filters.coords)

            # Crea una lista con distancias
            enriched_places = []
            for place in places:
                dist = haversine_distance(
                    lat_user, lng_user,
                    place.geolocation.lat,
                    place.geolocation.lng
                )
                enriched_places.append((dist, place))

            # Ordenar por distancia (de menor a mayor)
            enriched_places.sort(key=lambda x: x[0])

            # Devolver solo los objetos Place ya ordenados
            places = [p[1] for p in enriched_places]

        except Exception as e:
            print("Error al calcular distancias:", e)

    return places
