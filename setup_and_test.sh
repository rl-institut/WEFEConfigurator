#!/bin/bash
# Setup and test script for WEFEConfigurator survey

set -e  # Exit on error

echo "=========================================="
echo "WEFE Survey Setup & Test Script"
echo "=========================================="
echo ""

# Navigate to app directory
cd "$(dirname "$0")/app"

echo "Step 1: Checking Django installation..."
python -c "import django; print(f'✓ Django {django.get_version()} found')" || {
    echo "✗ Django not found! Make sure you've activated the conda environment:"
    echo "  conda activate WEFEConfigurator"
    exit 1
}

echo ""
echo "Step 2: Applying database migrations..."
python manage.py migrate

echo ""
echo "Step 3: Checking if survey questions exist..."
QUESTION_COUNT=$(python manage.py shell -c "from survey.models import SurveyQuestion; print(SurveyQuestion.objects.count())" 2>/dev/null || echo "0")

if [ "$QUESTION_COUNT" = "0" ]; then
    echo "No questions found. Populating database with survey questions..."
    python manage.py update_survey_questions
else
    echo "✓ Found $QUESTION_COUNT survey questions in database"
    echo "  (Run 'python manage.py update_survey_questions --update --dev' to update)"
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To test the water pump mapping:"
echo "1. Start the server:"
echo "   python manage.py runserver"
echo ""
echo "2. Visit: http://127.0.0.1:8000/view/survey/1"
echo ""
echo "3. Fill out the survey, including water pump questions:"
echo "   - Question 3: Select 'groundwater well'"
echo "   - Question 3_GW.1: 'Are water pumps required?' → Yes"
echo "   - Question 3_GW.1.1: Pump height → e.g., 25"
echo "   - Question 3_GW.1.4: Capacity → e.g., 10"
echo ""
echo "4. After submitting, export the answers:"
echo "   python manage.py save_survey_answers 1"
echo ""
echo "5. Check the JSON file:"
echo "   cat scenario_1_survey_answers.json | grep '3_GW'"
echo ""
echo "6. Build the scenario:"
echo "   cd ../component_library/scripts"
echo "   python build_scenario.py"
echo ""
echo "7. Verify the water pump component:"
echo "   cat ../../scenarios/scenario_1/data/elements/water_pumps.csv"
echo ""
