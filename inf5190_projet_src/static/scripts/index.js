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
    var st = $("#state");

    if (arr_validation(arrondissement)) {

        st.addClass("alert alert-primary d-flex align-items-center justify-content-between");
        st.append("Chargement des données en cours...<div class= \"loader\" ></div >")
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
            st.addClass("d-flex flex-column align-items-center justify-content-center");
            st.append("<h2>Aucun arrondissement trouvé<h2> <img src=\"../images/not_found.png\" style=\"height: 250px; width: 250px; \" alt=\"Not_Found\">");
            console.log(err);
        });
    }
}