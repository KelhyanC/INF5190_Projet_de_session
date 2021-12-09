var st = $("#state");

//Affiche un message d'erreur en fonction de la cause
function showError(why) {
    st.addClass("d-flex flex-column align-items-center justify-content-center");
    st.append(`<h2>${why}<h2> <img src=\"../images/not_found.png\" style=\"height: 250px; width: 250px; \" alt=\"Not_Found\">`);
}

//Affiche un loader lors d'une requete asynchrone
function showLoader() {
    st.removeClass();
    st.empty();
    st.addClass("alert alert-primary d-flex align-items-center justify-content-between");
    st.append("Chargement des données en cours...<div class= \"loader\" ></div >");
}

//Valide la saisie du formulaire du nom d'arrondissement
function arr_validation(input) {
    $("#arr_error").removeClass();
    $("#arr_error").empty();
    if (input.trim() == "") {
        $("#arr_error").addClass("alert alert-danger");
        $("#arr_error").append("Le champs ne peut pas être vide");
        return false;
    }
    return true;
}

//Affiche les installations par arrondissement sous forme de tableau
function getInstallationsByArr() {

    const arrondissement = String($('input[name="arrondissement"]').val());

    if (arr_validation(arrondissement)) {

        showLoader();

        fetch(`/api/installations?arrondissement=${arrondissement}`).then(rep => {
            st.removeClass();
            st.empty();
            if (!rep.ok) {
                throw Error(rep.statusText);
            }
            return rep.json();
        }).then(data => {
            tableau = `
                <table class="table table-striped table-hover my-2">
                    <caption></caption>
                    <thead class="thead-dark">
                        <th scope="col">Nom</th>
                        <th scope="col">Type d'installation</th>
                        <th></th>
                    </thead>
                    <tbody id="liste_arr">
                    </tbody>
                </table>
            `;
            st.append(tableau);
            $("caption").append(data[0].arrondissement);
            console.log("OK", data);
            data.forEach(arr => {
                $("#liste_arr").append(`
                <tr>
                    <td>${arr.nom}</td>
                    <td>${arr.type_installation}</td>
                    <td><a class="btn btn-secondary mr-2" href="/installation/${arr.id}">modifier</a><button class="btn btn-danger" onclick="deleteInstallation(${arr.id})">supprimer</button></td>
                </tr>
            `);
            });
        }).catch(err => {
            showError("Aucun arrondissement trouvé");
            console.log(err);
        });
    }
}

//Affiche les informations d'une installation en fonction de son ID
function getInstallationById() {
    input = $("#nom_installation").val();
    console.log(input);

    showLoader();

    fetch(`/api/installation/${input}`).then(rep => {
        st.removeClass();
        st.empty();
        if (!rep.ok) {
            throw Error(rep.statusText);
        }
        return rep.json();
    }).then(data => {
        details = `
                <table class="table table-primary table-striped mt-5">
                    <thead class="thead-dark">
                        <tr>
                            <th class="text-center" scope="row" colspan="2">${data.nom}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th scope="row">ID</th>
                            <td>${data.id}</td>
                        </tr>
                        <tr>
                            <th scope="row">Arrondissement</th>
                            <td>${data.arrondissement}</td>
                        </tr>
                        <tr>
                            <th scope="row">Type d'installation</th>
                            <td>${data.type_installation}</td>
                        </tr>
                        <tr>
                            <th scope="row">Date d'ajout</th>
                            <td>${data.ajout_bd}</td>
                        </tr>
                    </tbody>
                </table>
            `;
        st.append(details);
        console.log("OK", data);
    }).catch(err => {
        showError("Une erreur est survenue, veuillez réessayer");
        console.log(err);
    });
}

//Supprime une installation en fonction de son ID et affiche une confirmation
function deleteInstallation(id) {
    $("#status").removeClass();
    $("#status").empty();
    fetch(`/api/installation/${id}`, {
        method: 'DELETE'
    }).then(rep => {
        if (!rep.ok) {
            throw Error(rep.statusText);
        }
        return rep.json();
    }).then(data => {
        console.log(data);
        setTimeout(function () {
            $("#status").removeClass();
            $("#status").empty();
        }, 5000);
        $("#status").addClass("alert alert-success");
        $("#status").append(`L'installation <b>"${data.nom}"</b> a correctement été supprimée`);
        getInstallationsByArr();
    }).catch(err => {
        $("#status").addClass("alert alert-danger");
        $("#status").append(`Une erreur est survenue, l'installation n'a pas pu être supprimée`);
        console.log(err);
    });
}

//Verifie qu'un champs ne soit pas vide, lors de la modification d'une installation
function validation(input, tag) {
    var it = $(`#${tag}`);
    it.removeClass();
    it.empty();
    if (input.trim() == "") {
        it.addClass("alert alert-danger");
        it.append("Le champs ne peut pas être vide");
        return false;
    }
    return true;
}

//Modifie les informations d'une installation et affiche une confirmation
function editInstallation() {
    var status = $("#confirmation");
    status.removeClass();
    status.empty();
    var id = $("#id").val();
    var name = $("#nom").val();
    var type_inst = $("#type_installation").val();
    var val1 = validation(name, "err_nom");
    var val2 = validation(type_inst, "err_type");
    if (val1 && val2) {
        fetch(`/api/installation/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nom: name,
                type_installation: type_inst
            })
        }).then(rep => {
            if (!rep.ok) {
                throw Error(rep.statusText);
            }
            return rep.json();
        }).then(() => {
            $("#type_installation").attr('disabled', true);
            $("#nom").attr('disabled', true);
            $("#zeboutton").hide();
            status.addClass("alert alert-success");
            status.append("L'installation a bien été modifiée");
        }).catch(err => {
            status.addClass("alert alert-warning");
            status.append("Une erreur inattendue est survenue");
            console.log(err)
        });
    } else {
        status.addClass("alert alert-warning");
        status.append("L'installation n'a pas été modifiée");
    }
}