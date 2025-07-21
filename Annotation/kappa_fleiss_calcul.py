import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa
import csv

# Charger le fichier CSV
df = pd.read_csv('Copie_de_Annotation_31_03_2025_(pour Kappa_Fliess)2.csv', sep=';', quoting=csv.QUOTE_ALL, escapechar='\\', encoding='utf-8')

# Vérifier que toutes les colonnes attendues sont présentes
expected_columns = ['Alain_émotions', 'Alain_émotions 2', 'Anton_émotions', 'Anton_émotions 2', 'Tony_émotion', 'Tony_émotions 2']
for col in expected_columns:
    if col not in df.columns:
        raise ValueError(f"Colonne manquante : {col}")

# Convertir les colonnes d'émotions en numérique (NaN pour les valeurs invalides)
for col in expected_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    invalid_values = df[col][~df[col].isna() & ~df[col].between(1, 7)]
    if not invalid_values.empty:
        print(f"Valeurs invalides dans la colonne {col} : {invalid_values}")

# -----------------------------------
# Version 1 : Utiliser toutes les émotions (seulement les tweets avec 6 votes)
# -----------------------------------
print("Calcul du Kappa de Fleiss avec toutes les émotions (seulement les tweets avec 6 votes)")

contingency_all = []
skipped_tweets = 0
for index, row in df.iterrows():
    votes = row[['Alain_émotions', 'Alain_émotions 2', 'Anton_émotions', 'Anton_émotions 2', 'Tony_émotion', 'Tony_émotions 2']].dropna().astype(float)
    if len(votes) == 6:
        counts = [sum(votes == i) for i in range(1, 8)]
        contingency_all.append(counts)
    else:
        skipped_tweets += 1

print(f"Tweets analysés : {len(contingency_all)}")
print(f"Tweets exclus (moins ou plus de 6 votes) : {skipped_tweets}")

contingency_all_df = pd.DataFrame(contingency_all, columns=[1, 2, 3, 4, 5, 6, 7])
if not contingency_all_df.empty:
    kappa_all = fleiss_kappa(contingency_all_df, method='fleiss')
    print(f"Kappa de Fleiss (toutes émotions, 6 votes) : {kappa_all:.4f}")
else:
    print("Erreur : Aucun tweet n'a exactement 6 votes.")

print("\nTableau de contingence (premières lignes) :")
print(contingency_all_df.head())

# -----------------------------------
# Version optimisée : Maximiser l’accord en choisissant entre émotion 1 et émotion 2
# -----------------------------------
print("\nCalcul du Kappa de Fleiss (maximiser l’accord entre émotion 1 et émotion 2)")

contingency_optimized = []
for index, row in df.iterrows():
    # Récupérer les émotions 1 et 2 de chaque évaluateur
    alain_em1, alain_em2 = row['Alain_émotions'], row['Alain_émotions 2']
    anton_em1, anton_em2 = row['Anton_émotions'], row['Anton_émotions 2']
    tony_em1, tony_em2 = row['Tony_émotion'], row['Tony_émotions 2']

    # Vérifier que les émotions 1 sont présentes
    if pd.isna(alain_em1) or pd.isna(anton_em1) or pd.isna(tony_em1):
        print(f"Tweet {index} a un problème : émotion 1 manquante pour un évaluateur.")
        continue

    # Choisir le vote qui maximise l’accord pour chaque évaluateur
    final_votes = []
    for eval_em1, eval_em2, other_em1_1, other_em1_2 in [
        (alain_em1, alain_em2, anton_em1, tony_em1),  # Alain
        (anton_em1, anton_em2, alain_em1, tony_em1),  # Anton
        (tony_em1, tony_em2, alain_em1, anton_em1),   # Tony
    ]:
        # Par défaut, prendre l'émotion 1
        chosen_vote = eval_em1
        # Si l'émotion 2 existe, vérifier si elle est en accord avec les émotions 1 des autres
        if not pd.isna(eval_em2):
            # Compter les accords avec l'émotion 1
            em1_agreements = sum(1 for other in [other_em1_1, other_em1_2] if eval_em1 == other)
            # Compter les accords avec l'émotion 2
            em2_agreements = sum(1 for other in [other_em1_1, other_em1_2] if eval_em2 == other)
            # Si l'émotion 2 a plus d'accords, la choisir
            if em2_agreements > em1_agreements:
                chosen_vote = eval_em2
        final_votes.append(chosen_vote)

    # Vérifier qu'on a 3 votes
    votes = pd.Series(final_votes).dropna().astype(float)
    if len(votes) == 3:
        counts = [sum(votes == i) for i in range(1, 8)]
        contingency_optimized.append(counts)
    else:
        print(f"Tweet {index} a un problème : {len(votes)} votes au lieu de 3.")

# Convertir en DataFrame
contingency_optimized_df = pd.DataFrame(contingency_optimized, columns=[1, 2, 3, 4, 5, 6, 7])

# Calculer le Kappa de Fleiss
if not contingency_optimized_df.empty:
    kappa_optimized = fleiss_kappa(contingency_optimized_df, method='fleiss')
    print(f"Kappa de Fleiss (maximiser l’accord) : {kappa_optimized:.4f}")
else:
    print("Erreur : Aucun tweet valide pour maximiser l’accord.")

print("\nTableau de contingence (premières lignes, maximiser l’accord) :")
print(contingency_optimized_df.head())

# -----------------------------------
# Version 1 bis : Utiliser un vote par évaluateur (priorité à émotion 1)
# -----------------------------------
print("\nCalcul du Kappa de Fleiss avec un vote par évaluateur (priorité à émotion 1)")

contingency_combined = []
for index, row in df.iterrows():
    alain_vote = row['Alain_émotions'] if not pd.isna(row['Alain_émotions']) else row['Alain_émotions 2']
    anton_vote = row['Anton_émotions'] if not pd.isna(row['Anton_émotions']) else row['Anton_émotions 2']
    tony_vote = row['Tony_émotion'] if not pd.isna(row['Tony_émotion']) else row['Tony_émotions 2']
    votes = pd.Series([alain_vote, anton_vote, tony_vote]).dropna().astype(float)
    if len(votes) == 3:
        counts = [sum(votes == i) for i in range(1, 8)]
        contingency_combined.append(counts)
    else:
        print(f"Tweet {index} a un problème : {len(votes)} votes au lieu de 3.")

contingency_combined_df = pd.DataFrame(contingency_combined, columns=[1, 2, 3, 4, 5, 6, 7])
if not contingency_combined_df.empty:
    kappa_combined = fleiss_kappa(contingency_combined_df, method='fleiss')
    print(f"Kappa de Fleiss (un vote par évaluateur) : {kappa_combined:.4f}")
else:
    print("Erreur : Aucun tweet valide pour un vote par évaluateur.")

print("\nTableau de contingence (premières lignes, un vote par évaluateur) :")
print(contingency_combined_df.head())

# -----------------------------------
# Version 2 : Utiliser seulement l'émotion 1 de chaque évaluateur
# -----------------------------------
print("\nCalcul du Kappa de Fleiss avec seulement l'émotion 1")

contingency_em1 = []
for index, row in df.iterrows():
    votes = row[['Alain_émotions', 'Anton_émotions', 'Tony_émotion']].dropna().astype(float)
    if len(votes) == 3:
        counts = [sum(votes == i) for i in range(1, 8)]
        contingency_em1.append(counts)
    else:
        print(f"Tweet {index} a un problème : {len(votes)} votes au lieu de 3 pour l'émotion 1.")

contingency_em1_df = pd.DataFrame(contingency_em1, columns=[1, 2, 3, 4, 5, 6, 7])
if not contingency_em1_df.empty:
    kappa_em1 = fleiss_kappa(contingency_em1_df, method='fleiss')
    print(f"Kappa de Fleiss (émotion 1 uniquement) : {kappa_em1:.4f}")
else:
    print("Erreur : Aucun tweet valide pour l'émotion 1.")

print("\nTableau de contingence (premières lignes, émotion 1) :")
print(contingency_em1_df.head())

# -----------------------------------
# Bonus : Générer un fichier avec les annotations définitives
# -----------------------------------
print("\nGénération des annotations définitives (émotion majoritaire)")

# Fonction pour trouver l'émotion majoritaire (toutes émotions)
def get_majority_emotion(row):
    votes = row[['Alain_émotions', 'Alain_émotions 2', 'Anton_émotions', 'Anton_émotions 2', 'Tony_émotion', 'Tony_émotions 2']].dropna().astype(float)
    if len(votes) == 0:
        return None
    mode = votes.mode()
    return mode[0] if not mode.empty else None

# Fonction pour trouver l'émotion majoritaire (émotion 1 uniquement)
def get_majority_emotion_em1(row):
    votes = row[['Alain_émotions', 'Anton_émotions', 'Tony_émotion']].dropna().astype(float)
    if len(votes) == 0:
        return None
    mode = votes.mode()
    return mode[0] if not mode.empty else None

# Fonction pour trouver l'émotion majoritaire (maximiser l’accord)
def get_majority_emotion_optimized(row):
    alain_em1, alain_em2 = row['Alain_émotions'], row['Alain_émotions 2']
    anton_em1, anton_em2 = row['Anton_émotions'], row['Anton_émotions 2']
    tony_em1, tony_em2 = row['Tony_émotion'], row['Tony_émotions 2']
    if pd.isna(alain_em1) or pd.isna(anton_em1) or pd.isna(tony_em1):
        return None

    final_votes = []
    for eval_em1, eval_em2, other_em1_1, other_em1_2 in [
        (alain_em1, alain_em2, anton_em1, tony_em1),
        (anton_em1, anton_em2, alain_em1, tony_em1),
        (tony_em1, tony_em2, alain_em1, anton_em1),
    ]:
        chosen_vote = eval_em1
        if not pd.isna(eval_em2):
            em1_agreements = sum(1 for other in [other_em1_1, other_em1_2] if eval_em1 == other)
            em2_agreements = sum(1 for other in [other_em1_1, other_em1_2] if eval_em2 == other)
            if em2_agreements > em1_agreements:
                chosen_vote = eval_em2
        final_votes.append(chosen_vote)

    votes = pd.Series(final_votes).dropna().astype(float)
    if len(votes) == 0:
        return None
    mode = votes.mode()
    return mode[0] if not mode.empty else None

# Ajouter les colonnes pour les émotions majoritaires
if 'emotion_majoritaire_toutes' not in df.columns:
    df['emotion_majoritaire_toutes'] = df.apply(get_majority_emotion, axis=1)
if 'emotion_majoritaire_em1' not in df.columns:
    df['emotion_majoritaire_em1'] = df.apply(get_majority_emotion_em1, axis=1)
if 'emotion_majoritaire_optimisée' not in df.columns:
    df['emotion_majoritaire_optimisée'] = df.apply(get_majority_emotion_optimized, axis=1)

# Sauvegarder le résultat dans un nouveau CSV
df.to_csv('resultats_avec_emotion_majoritaire.csv', sep=';', index=False)
print("Un fichier 'resultats_avec_emotion_majoritaire.csv' a été créé avec les émotions majoritaires (toutes émotions, émotion 1, optimisée).")