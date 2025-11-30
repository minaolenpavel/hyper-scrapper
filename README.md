# Hyper Scrapper (Obsolete)

**⚠️ Attention : Ce projet est maintenant obsolète** – Les salles de cours sont désormais systématiquement fermées à clé et je ne sais pas exactement pourquoi le script plante maintenant. Mais voici pour la postérité ce petit projet Python fait pour l’été.

---

## Description

Ce script Python avait pour but de :

1. Scraper le planning public de la fac (Inalco).
2. Déterminer quelles salles étaient libres en fonction des cours programmés.

Principe simple : si aucune activité n’était prévue dans une salle, alors elle était libre. L’idée était de créer une **liste de salles libres**, parce que ça n’existait pas et que ça aurait été pratique pour travailler ou réviser.

Le script marchait plutôt bien à l’époque, mais je n’ai jamais pu vérifier sa précision en période normale.

---

## Fonctionnalités

* Scraping des plannings via Python.
* Calcul automatique des **salles libres**.
  
---

## Utilisation

À l’époque :

1. Lancer le script principal `Program.py`.
2. Le script analysait tous les cours, toutes les salles, et renvoyait une liste des salles libres.
3. Admirer la magie de Python et rêver aux salles vides.

```bash
python Program.py
```

---

## Limitations

* Obsolète → les salles sont désormais fermées à clé et le script plante pour des raisons inconnues.
* Testé uniquement en période estivale → exactitude non garantie en période normale.
* Script trop long à l'éxecution → code fonctionnel mais pas optimisé pour un usage sérieux.

---
