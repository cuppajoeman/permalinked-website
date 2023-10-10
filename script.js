const urlParams = new URLSearchParams(window.location.search);
const requestedUUID = urlParams.get('uuid');

if (requestedUUID != null) {
    fetch("uuid_to_paths.json")
        .then(response => response.json())
        .then(json => {
            if (requestedUUID in json) {
                let contentPath = json[requestedUUID];
                window.location.href = contentPath;
            } else {
                document.body.innerText = "the request for a file with a uuid of : " + requestedUUID + " doesn't exist."
            }
        });

}
