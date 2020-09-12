function changeSelectMdp() {
  var mdp_select = document.getElementById("mdp_select").value
  var helpers = {
    'fixe': 'Le même pour tous les participants',
    'aleatoire': 'Alphanumérique au hasard',
    'prenom': 'Exemple: georges'
  }
  document.getElementById('mdp-select-id').innerHTML = helpers[mdp_select]
  if (mdp_select == "fixe"){
    document.getElementById("mdp_fixe").style.display = "inline-block";
    document.getElementById("mdp_longueur").style.display = "None";
  }
  else if (mdp_select == "aleatoire"){
    document.getElementById("mdp_fixe").style.display = "None";
    document.getElementById("mdp_longueur").style.display = "inline-block";
  }
  else{//prénom
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
  // on retourne donc true et active le boutons
  document.getElementById('preview-button').disabled = false
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
    // désactive  le boutons
    document.getElementById('preview-button').disabled = true

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

function testLength(input) {
  // Vérifie que la longueur d'une chaine de caractère est comprise entre 4 et 16.
  // Retourne une chaine de caractère:
  // - 'trop court: moins de 4'
  // - 'trop long: plus de 16'
  // - chaine vide si aucun problème
  if (input.length < 4){
    return 'trop court: moins de 4'
  }
  if (input.length > 16){
    return 'trop long: plus de 16'
  }
  return ''
}

function tableToJson(table) {
  // Convertit le tableau html en json et teste les erreurs sur les champs login et password
  var data = []; // first row needs to be headers
  var headers = ['login', 'lastname', 'firstname', 'password'];
  // go through rows
  for (var i=1; i<table.rows.length; i++) {
    var tableRow = table.rows[i];
    var rowData = {};
    // go through row cells
    for (var j=0; j<tableRow.cells.length; j++) {
      var cell = tableRow.cells[j]
      var value = cell.childNodes[0].nodeValue.replace(/\n/g, '').trim()
      // Si on a un champ de type login ou password, on gère les erreurs
      if (j == 0 || j == 3){
        var error = testLength(value)
        // on retire les possibles messages d'erreurs
        while (cell.childNodes.length > 1) {
          cell.removeChild(cell.lastChild);
        }
        if (error === ""){// pas d'erreur
          cell.classList.remove('has-text-danger', 'has-text-weight-bold', 'tooltip', 'tooltip-right', 'tooltip-left')
        }
        else { // erreur
          cell.classList.add('has-text-danger', 'has-text-weight-bold', 'tooltip')
          if (j == 0){
            cell.classList.add('tooltip-left')
          }
          else{
            cell.classList.add('tooltip-right')
          }
          var tooltip = document.createElement("span");
          tooltip.classList.add("tooltiptext", "notification", "is-warning")
          tooltip.innerHTML =  error
          cell.appendChild(tooltip)
        }
      }
      rowData[ headers[j] ] = value;
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
