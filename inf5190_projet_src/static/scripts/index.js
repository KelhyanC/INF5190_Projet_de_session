var st = $("#state");

function showError(why) {
    st.addClass("d-flex flex-column align-items-center justify-content-center");
    st.append(`<h2>${why}<h2> <img src=\"../images/not_found.png\" style=\"height: 250px; width: 250px; \" alt=\"Not_Found\">`);
}

function showLoader() {
    st.removeClass();
    st.empty();
    st.addClass("alert alert-primary d-flex align-items-center justify-content-between");
    st.append("Chargement des données en cours...<div class= \"loader\" ></div >");
}

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
                    <td><a class="btn btn-secondary mr-2" href="#">modifier</a><a class="btn btn-danger" href="#">supprimer</a></td>
                </tr>
            `);
            });
        }).catch(err => {
            showError("Aucun arrondissement trouvé");
            console.log(err);
        });
    }
}

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