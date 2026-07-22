# test_vision.py
import sys


from app.services.vision_service import VisionService  

def test_extraction():
    print("⏳ Initialisation du service Vision...")
    try:
        service = VisionService()
        
        # Nom de l'image présente dans ton dossier uploads/raw/
        image_a_tester = "matelas_02.jpeg" 
        
        print(f"📸 Analyse de l'image : {image_a_tester}...")
        resultat = service.analyze(image_a_tester)
        
        print("\n✅ Analyse réussie ! Voici le résultat extrait :")
        print("-" * 40)
        # .model_dump() ou .dict() selon ta version de Pydantic pour un affichage propre
        import pprint
        pprint.pprint(resultat.model_dump())
        print("-" * 40)

    except FileNotFoundError as e:
        print(f"\n❌ Erreur de fichier : {e}")
        print("Vérifie que ton image est bien placée dans 'uploads/raw/'")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue lors de l'appel à l'API : {e}")

if __name__ == "__main__":
    test_extraction()