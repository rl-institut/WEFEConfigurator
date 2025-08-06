function deselect(elm) {
    if (elm.checked == true) {
    elm.click();
    }
}

function getSelectedValues(inputElement) {
    var stray = [];
    if(new_value.type == "checkbox"){
        var checkBoxes = new_value.parentElement.parentElement.querySelectorAll('input[type="checkbox"]'); // get all the check box
        checkBoxes.forEach(item => {if (item.checked){stray.push(item.value);}})
    }
    else{
        var array_opts = Object.values(new_value.selectedOptions);
        stray = array_opts.map((o)=> o.value);
    }
    // selected options
    return stray
}

function getRelevantSubQuestions(selectedValues, subQuestionMapping) {
    var subQuestions = [];
    selectedValues.filter((r) => {
        // select only potential subquestions
        return r in subQuestionMapping;
    }).map((o)=>{
      // if there are more than one subquestion, expands their numbers
        if( typeof subQuestionMapping[o] != "string"){
            subQuestionMapping[o].map((e)=>{subQuestions.push(e);});
        }
        else{subQuestions.push(subQuestionMapping[o]);}
    });

    return subQuestions;
}

function toggleVisibility(elementIdPrefix, subQuestions, subQuestionMapping) {
    for (let key in subQuestionMapping) {
        if(typeof subQuestionMapping[key] === 'string' || subQuestionMapping[key] instanceof String){
            var q_id = [subQuestionMapping[key]];
        }
        else{q_id=subQuestionMapping[key]}

        // loop over the subquestions
        for (let key_i in q_id){
            var subQuestionDiv = document.getElementById(elementIdPrefix + q_id[key_i]);
            if(subQuestionDiv === null){
                console.log("Looking for element " + elementIdPrefix + q_id[key_i]);
            }
            else{

                var dropdowns = subQuestionDiv.querySelectorAll(".sub_question");

                var check_boxes = subQuestionDiv.querySelectorAll('input[type="checkbox"]');

                if(subQuestions.includes(q_id[key_i])){
                    // show the subquestion
                    subQuestionDiv.parentNode.classList.remove("disabled");
                }
                else{
                    // hide the subquestion
                    subQuestionDiv.parentNode.classList.add("disabled");
                    // deselect the checked options of subquestions
                    if(check_boxes){
                        for(let i=0;i<check_boxes.length;i++){
                            deselect(check_boxes[i]);
                        }
                    }
                }
            }
        }
    }
}


function triggerSubQuestion(new_value,subQuestionMapping){
    console.log("Trigger Sub Question " + new_value.name);
    let selectedValues = getSelectedValues(new_value);
    let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);
    toggleVisibility("div_id_criteria_", subQuestions, subQuestionMapping);
}


function hasClassStartingWith(element, prefix) {
    return Array.from(element.classList).some(className => className.startsWith(prefix));
}

function resetMatrixRows(container, selectedValues) {


}

function triggerMatrixSubQuestion(new_value, subQuestionMapping) {
    console.log("Trigger Matrix Sub Question");
    let selectedValues = getSelectedValues(new_value);
    //let subQuestions = getRelevantSubQuestions(selectedValues, subQuestionMapping);

    //toggleMatrixVisibility(matrixId='id_matrix_' + new_value.name, elementIdPrefix="id_criteria_", subQuestions, subQuestionMapping);
    //
    const container = document.getElementById('id_matrix_' + new_value.name);

      const visibleRowData = [];
  // Look for all label spans inside this container
  container.querySelectorAll(".matrix_col_1").forEach(label => {

    const cropName = label.textContent.trim().toLowerCase();
    const rowClass = Array.from(label.classList).find(cls => cls.startsWith("label_row_"));

    if (selectedValues.includes(cropName)) {
      visibleRowData.push({ crop: cropName ,rowClass});
    }
  });

  // Hide all rows and remove their existing matrix_row_N classes
    container.querySelectorAll(".matrix_target").forEach(el => {
      // only remove the rows and not the headers
      if(hasClassStartingWith(el, "label_row") === true){
          el.style.display = "none";
          el.disabled = true;
          el.classList.remove(...Array.from(el.classList).filter(cls => cls.startsWith("matrix_row")));
      }
    });

  // Reassign grid-row classes starting from 1
  visibleRowData.forEach((row, index) => {
    const newClass = `matrix_row_${index + 1}`;
    container.querySelectorAll("." + row.rowClass).forEach(el => {
      el.style.display = "";
      if (el.tagName === "INPUT") el.disabled = false;
      if (el.tagName === "SELECT") el.disabled = false;
      el.classList.add(newClass);
    });
  });

  // display the headers only if there are selected elements
  hide_parent_container = true;

  container.querySelectorAll(".matrix_row_0").forEach(el => {
    if (visibleRowData.length === 0) {
        el.style.display = "none";
    }else{
        el.style.display = "";
        hide_parent_container = false;
    }
  });
  if(hide_parent_container){
    container.classList.add("disabled");
  }
  else{
  container.classList.remove("disabled");
  //
  }
    //resetMatrixRows(container=matrixDiv, selectedValues=selectedValues)
}

var surveyFormDOM = document.getElementById("surveyQuestions");

const allElements = document.querySelectorAll('*');
const elementsWithOnchange = Array.from(allElements).filter(el => el.hasAttribute('onchange'));

console.log(elementsWithOnchange);

elementsWithOnchange.forEach(input => {
    input.dispatchEvent(new Event("change", { bubbles: true }));
});// this is not compatible with saved data

console.log(document.querySelector('.checkbox-grid'))

/*var subQuestions = surveyFormDOM.querySelectorAll(".subquestion");
for(i=0;i<subQuestions.length;++i) {
    if(subQuestions[i].classList.contains("disabled"))
    {
        subQuestions[i].hidden = true;
        subQuestions[i].classList.remove("disabled")
    }
    else
    {
        subQuestions[i].hidden = false;
        subQuestions[i].classList.add("disabled")

    }
};*/
