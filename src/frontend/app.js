document.getElementById('fitnessForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const userInput = {
        age: parseInt(document.getElementById('age').value),
        weight: parseFloat(document.getElementById('weight').value),
        height: parseInt(document.getElementById('height').value),
        gender: document.getElementById('gender').value,
        activity_level: document.getElementById('activity_level').value,
        goal: document.getElementById('goal').value
    };
    
    try {
        const response = await fetch('http://localhost:8000/api/fitness-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userInput),
        });
         console.log("server response", response)
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();

        console.log("data from backend service", data)
        
        // Show results
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        // alert('An error occurred. Please try again.');
    }
});

function displayResults(data) {
    document.getElementById('results').style.display = 'block';
  
    // Display prediction results
    const predictionResults = document.getElementById('predictionResults');
    predictionResults.innerHTML = `
      <p><strong>Target Calories:</strong> ${data.predictions.target_calories} kcal</p>
      <p><strong>Protein Ratio:</strong> ${data.predictions.protein_ratio} %</p>
      <p><strong>Carb Ratio:</strong> ${data.predictions.carb_ratio} %</p>
      <p><strong>Fat Ratio:</strong> ${data.predictions.fat_ratio} %</p>
      <p><strong>Exercise Intensity:</strong> ${data.predictions.exercise_intensity}</p>
    `;
  
    // Display exercise plan
    const exercisePlan = document.getElementById('exercisePlan');
    exercisePlan.innerHTML = '';
    data.exercise_plan.forEach((day) => {
      const dayEl = document.createElement('div');
      dayEl.innerHTML = `
        <h4>${day.day} - ${day.focus}</h4>
        <ul>
          ${day.exercises.map((exercise) => `
            <li>${exercise.name} - Sets: ${exercise.sets}, Reps: ${exercise.reps}, Rest: ${exercise.rest}s</li>
          `).join('')}
        </ul>
      `;
      exercisePlan.appendChild(dayEl);
    });
  
    // Display meal plan
    const mealPlan = document.getElementById('mealPlan');
    mealPlan.innerHTML = '';
    data.meal_plan.forEach((meal) => {
      const mealEl = document.createElement('div');
      mealEl.innerHTML = `
        <h4>${meal.meal_name}</h4>
        <ul>
          ${Object.entries(meal.foods).map(([food, grams]) => `
            <li>${food} - ${grams}g</li>
          `).join('')}
        </ul>
        <p>Total Calories: ${meal.total_calories}</p>
      `;
      mealPlan.appendChild(mealEl);
    });
  }
