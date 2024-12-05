
---

## **Présentation du Projet : Catégorisation des Clients par Achats**

### **Objectif :**
Permettre d'identifier la **catégorie prédominante** des achats d'un client en fonction de ses tendances d'achat. Cela est accompli en regroupant les achats par catégorie de produits et en déterminant celle qui a la quantité totale la plus élevée, tout en prenant en compte des seuils configurables.

---

## **Fonctionnalités principales :**

1. **Visualisation des Achats des Clients :**
   - Affichage des catégories de produits achetés par chaque client.
   - Quantités totales associées à chaque catégorie.

2. **Catégorie Prédominante :**
   - Calcul automatique de la catégorie prédominante d'un client selon ses achats.
   - Seuil configurable par client pour définir la catégorie prédominante.

3. **Configuration Personnalisable :**
   - Module pour définir les seuils spécifiques par client.
   - Interface intuitive pour gérer les configurations via Odoo.

4. **Navigation Simplifiée :**
   - Menu dédié aux rapports de ventes personnalisés et à la configuration.
   - Filtrage et regroupement par clients directement dans l'interface.

---

## **Architecture Technique :**

1. **Modèles :**
   - **`sale.report` :** Étendu pour inclure les champs de catégorisation et de calculs.
   - **`sale.category.config` :** Nouveau modèle pour gérer les seuils configurables.

2. **Calculs Dynamiques :**
   - Utilisation de méthodes `@api.depends` pour calculer les achats et la catégorie prédominante en temps réel.

3. **Vues :**
   - Vues en liste et formulaires pour afficher les rapports et gérer les configurations.
   - Organisation en menus hiérarchiques sous un menu principal "Customers - Employees".

4. **Sécurité et Contraintes :**
   - Contrôles SQL pour garantir l'unicité des configurations par client et la validité des seuils.

---

## **Exemple d'utilisation en démo :**

1. **Configurer un seuil pour un client :**
   - Aller dans le menu "Configuration des Catégories".
   - Créer ou modifier une configuration en définissant un seuil.

2. **Afficher les catégories prédominantes :**
   - Naviguer vers "Predominant customers".
   - Filtrer les clients pour voir leurs catégories prédominantes et quantités associées.

3. **Analyse des données :**
   - Utiliser le regroupement ou les filtres dans Odoo pour analyser les achats par catégorie.

---

## Fonctionnalités
- Calcul automatique des catégories prédominantes.
- Seuil configurable par client.
- Rapport détaillé des catégories et quantités achetées.
- Interface utilisateur intuitive.

## Utilisation
1. Configurez les seuils des catégories dans "Configuration des Catégories".
2. Consultez les rapports dans "Predominant customers".

## Dépendances
- Odoo 15+ (ou version utilisée dans votre environnement).
- Module de base "Sale".

## Auteur
- [MAHERY NOMENA Freddy]
- Contact : [nomenamaheryfreddy@gmail.com]
  
