// Replace with your Spoonacular API key
const API_KEY = "6486e3ce28824304a20dbdd58a39693e";

// Event listener for the button click
document.getElementById('findRecipes').addEventListener('click', async () => {
  const ingredients = document.getElementById('ingredients').value.trim();
  if (!ingredients) {
    alert("Please enter some ingredients!");
    return;
  }

  // Show loading spinner
  document.getElementById('loading').style.display = 'block';

  const recipes = await fetchRecipes(ingredients);
  displayRecipes(recipes);

  // Hide loading spinner after recipes are displayed
  document.getElementById('loading').style.display = 'none';
});

// Fetch recipes from Spoonacular API
async function fetchRecipes(ingredients) {
  const url = `https://api.spoonacular.com/recipes/findByIngredients?ingredients=${encodeURIComponent(
    ingredients
  )}&number=5&apiKey=${API_KEY}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to fetch recipes");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    alert("Error fetching recipes. Please try again later.");
    return [];
  }
}

// Fetch detailed recipe information (including instructions) by recipe ID
async function fetchRecipeDetails(recipeId) {
  const url = `https://api.spoonacular.com/recipes/${recipeId}/information?apiKey=${API_KEY}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to fetch recipe details");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

// Display recipes in the popup
async function displayRecipes(recipes) {
  const recipesDiv = document.getElementById('recipes');
  recipesDiv.innerHTML = "";

  if (recipes.length === 0) {
    recipesDiv.innerHTML = "<p>No recipes found. Try different ingredients!</p>";
    return;
  }

  for (const recipe of recipes) {
    // Fetch detailed recipe information (including instructions)
    const recipeDetails = await fetchRecipeDetails(recipe.id);

    if (recipeDetails) {
      const recipeDiv = document.createElement('div');
      recipeDiv.classList.add('recipe-card');
      recipeDiv.innerHTML = `
        <div class="recipe-header">
          <h3>
            <a href="https://spoonacular.com/recipes/${recipe.title.replace(
              / /g,
              "-"
            )}-${recipe.id}" target="_blank" rel="noopener noreferrer">
              ${recipe.title}
            </a>
          </h3>
          <img class="recipe-img" src="${recipe.image}" alt="${recipe.title}" />
        </div>
        <div class="recipe-body">
          <h4>Instructions:</h4>
          <p>${recipeDetails.instructions || "No instructions available."}</p>
        </div>
      `;
      recipesDiv.appendChild(recipeDiv);
    }
  }
}
