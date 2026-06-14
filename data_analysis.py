import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('All_Diets.csv')
df.columns = df.columns.str.strip()
df['Protein(g)'] = pd.to_numeric(df['Protein(g)'], errors='coerce')
df['Carbs(g)'] = pd.to_numeric(df['Carbs(g)'], errors='coerce')
df['Fat(g)'] = pd.to_numeric(df['Fat(g)'], errors='coerce')
df['Protein(g)'] = df['Protein(g)'].fillna(df['Protein(g)'].mean())
df['Carbs(g)'] = df['Carbs(g)'].fillna(df['Carbs(g)'].mean())
df['Fat(g)'] = df['Fat(g)'].fillna(df['Fat(g)'].mean())

print("Dataset loaded successfully!")
print(f"Total recipes: {len(df)}")
print(f"Diet types: {df['Diet_type'].unique()}")

print("\n--- Average Macronutrients per Diet Type ---")
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean().round(2)
print(avg_macros)

print("\n--- Top 5 Protein-Rich Recipes per Diet Type ---")
top_protein = df.groupby('Diet_type').apply(lambda x: x.nlargest(5, 'Protein(g)')[['Recipe_name', 'Protein(g)']]).reset_index(drop=True)
print(top_protein)

print("\n--- Diet Type with Highest Average Protein ---")
highest_protein = avg_macros['Protein(g)'].idxmax()
print(f"{highest_protein}: {avg_macros['Protein(g)'].max():.2f}g")

print("\n--- Most Common Cuisine per Diet Type ---")
common_cuisine = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.value_counts().index[0])
print(common_cuisine)

df['Protein_to_Carbs_ratio'] = (df['Protein(g)'] / df['Carbs(g)']).round(2)
df['Carbs_to_Fat_ratio'] = (df['Carbs(g)'] / df['Fat(g)']).round(2)
print("\n--- New Ratio Columns Added ---")
print(df[['Recipe_name', 'Protein_to_Carbs_ratio', 'Carbs_to_Fat_ratio']].head(10))

avg_macros.plot(kind='bar', figsize=(10, 6))
plt.title('Average Macronutrient Content by Diet Type')
plt.xlabel('Diet Type')
plt.ylabel('Grams')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('bar_chart.png')
plt.close()
print("\nBar chart saved!")

plt.figure(figsize=(8, 5))
sns.heatmap(avg_macros, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Macronutrient Heatmap by Diet Type')
plt.tight_layout()
plt.savefig('heatmap.png')
plt.close()
print("Heatmap saved!")

top5 = df.nlargest(25, 'Protein(g)')
plt.figure(figsize=(10, 6))
colors = ['blue', 'red', 'green', 'orange', 'purple']
diets = df['Diet_type'].unique().tolist()
for i, diet in enumerate(diets):
    subset = top5[top5['Diet_type'] == diet]
    plt.scatter(subset['Cuisine_type'].tolist(), subset['Protein(g)'].tolist(), label=diet, color=colors[i], s=100)
plt.title('Top 5 Protein-Rich Recipes by Cuisine Type')
plt.xlabel('Cuisine Type')
plt.ylabel('Protein (g)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig('scatter_plot.png')
plt.close()
print("Scatter plot saved!")

print("\nAll done! Check project1 folder for the charts.")
