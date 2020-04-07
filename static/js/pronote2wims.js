function changeSelectMdp() {
  var mdp_select = document.getElementById("mdp_select").value
  if (mdp_select == "fixe"){
    document.getElementById("mdp_fixe").style.display = "inline-block";
    document.getElementById("mdp_longueur").style.display = "None";

  }
  else if (mdp_select == "aleatoire"){
    document.getElementById("mdp_fixe").style.display = "None";
    document.getElementById("mdp_longueur").style.display = "inline-block";
  }
  else{
    document.getElementById("mdp_fixe").style.display = "None";
    document.getElementById("mdp_longueur").style.display = "None";
  }
};

function changeSelectId() {
  var id_select = document.getElementById("id_select").value
  if (id_select == "custom"){
    document.getElementById("format_id_custom").style.display = "inline-block";
    document.getElementById("format_id_custom_help").style.display = "inline-block";
    document.getElementById("exemple_prenomnom").style.display = "None";
    document.getElementById("exemple_pnom").style.display = "None";
    document.getElementById("exemple_nomp").style.display = "None";
  }
  else if (id_select == "prenomnom"){
    document.getElementById("format_id_custom").style.display = "None";
    document.getElementById("format_id_custom_help").style.display = "None";
    document.getElementById("exemple_prenomnom").style.display = "inline-block";
    document.getElementById("exemple_pnom").style.display = "None";
    document.getElementById("exemple_nomp").style.display = "None";
  }
  else if (id_select == "nomp"){
    document.getElementById("format_id_custom").style.display = "None";
    document.getElementById("format_id_custom_help").style.display = "None";
    document.getElementById("exemple_prenomnom").style.display = "None";
    document.getElementById("exemple_pnom").style.display = "None";
    document.getElementById("exemple_nomp").style.display = "inline-block";
  }
  else{
    document.getElementById("format_id_custom").style.display = "None";
    document.getElementById("format_id_custom_help").style.display = "None";
    document.getElementById("exemple_prenomnom").style.display = "None";
    document.getElementById("exemple_pnom").style.display = "inline-block";
    document.getElementById("exemple_nomp").style.display = "None";
  }
};

//https://github.com/chintanbanugaria/bulma-file-upload/blob/master/index.html
var file = document.getElementById("file");
file.onchange = function(){
  if(file.files.length > 0)
  {
    document.getElementById('filename').innerHTML = file.files[0].name;
  }
};

function validateForm(){
  // vérifie le formulaire avant de l'envoyer
  var mdp_select = document.getElementById("mdp_select").value
  if (mdp_select == "fixe"){
    return validateMdpFixe()
  }
  // Le mot de passe fixe est la seule vérification (pour l'instant)
  // on retourne donc true et active les boutons
  document.getElementById('preview-button').disabled = false
  document.getElementById('upload-button').disabled = false
  return true;
}

function validateMdpFixe(){
  // On va seulement tester si mdp < 4 car l'input a maxlength="16"
  var element = document.getElementById("mdp_fixe_input")
  if (element.value.length < 4){
    // met le champ en rouge
    element.classList.add("is-danger")
    // affiche les avertissements
    var warnings = document.getElementsByClassName("mdp-fixe-warning")
    for(var i = 0; i < warnings.length; i++){
      warnings[i].classList.remove('is-invisible')
    }
    // désactive  les boutons
    document.getElementById('preview-button').disabled = true
    document.getElementById('upload-button').disabled = true

    return false
  } else {
    // le contraire
    element.classList.remove("is-danger")
    element.classList.add("is-success")
    var warnings = document.getElementsByClassName("mdp-fixe-warning")
    for(var i = 0; i < warnings.length; i++){
      warnings[i].classList.add('is-invisible')
    }
    document.getElementById('preview-button').disabled = false
    document.getElementById('upload-button').disabled = false
    return true
  }
}

function toggleTabs(tabName){
  // set active to clicked tab and show/hide content
  var tabTools = document.getElementById('tab-tools')
  var tabHelp = document.getElementById('tab-help')
  var contentTools = document.getElementById('tools-content')
  var contentHelp = document.getElementById('help-content')


  if (tabName=='tools'){
    tabTools.classList.add('is-active')
    tabHelp.classList.remove('is-active')
    contentTools.classList.remove('is-hidden')
    contentHelp.classList.add('is-hidden')
  } else {
    tabTools.classList.remove('is-active')
    tabHelp.classList.add('is-active')
    contentTools.classList.add('is-hidden')
    contentHelp.classList.remove('is-hidden')
  }
}

function tableToJson(table) {
  var data = []; // first row needs to be headers
  var headers = ['login', 'lastname', 'firstname', 'password'];
  // go through cells
  for (var i=1; i<table.rows.length; i++) {
    var tableRow = table.rows[i];
    var rowData = {};
    for (var j=0; j<tableRow.cells.length; j++) {
      rowData[ headers[j] ] = tableRow.cells[j].childNodes[0].nodeValue.replace(/\n/g, '').trim();
    } data.push(rowData);
  }
  return data;
}

// Gère les modifications du tableau

document.querySelectorAll('.editable').forEach((cell, i) => {
  cell.addEventListener('keydown', function(event){
    // perd le focus si l'utilisateur appuie sur la touche entrée
    var key = event.keyCode || event.charCode;  // ie||others
    if(key == 13)  // if enter key is pressed
    event.target.blur();  // lose focus
  });
  cell.addEventListener('blur', function(event){
    // met à jour le json
    var json = tableToJson(document.getElementById('wims-table'))
    document.querySelectorAll('.wims-json').forEach((element) => {
      element.value = JSON.stringify(json)
    });

  });

});
