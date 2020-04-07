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
  return true;
}

function validateMdpFixe(){
  // On va seulement tester si mdp < 4 car l'input a maxlength="16"
  var element = document.getElementById("mdp_fixe_input")
  if (element.value.length < 4){
    element.classList.add("is-danger")
    var warnings = document.getElementsByClassName("mdp-fixe-warning")
    for(var i = 0; i < warnings.length; i++){
      warnings[i].classList.remove('is-invisible')
    }
    return false
  } else {
    element.classList.remove("is-danger")
    element.classList.add("is-success")
    var warnings = document.getElementsByClassName("mdp-fixe-warning")
    for(var i = 0; i < warnings.length; i++){
      warnings[i].classList.add('is-invisible')
    }
    return true
  }
}
