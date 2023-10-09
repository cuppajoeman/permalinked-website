let relativeContentDirectory

fetch("configuration.json")
    .then(response => response.json())
    .then(json => {
        let has_proper_configuration_file = "content_directory_relative_to_this_file" in json
        console.assert(has_proper_configuration_file)
        relativeContentDirectory = json["content_directory_relative_to_this_file"];
    });

const urlParams = new URLSearchParams(window.location.search);
const requestedUUID = urlParams.get('uuid');

if (requestedUUID != null) {
    fetch("uuid_to_paths.json")
        .then(response => response.json())
        .then(json => {
            if (requestedUUID in json) {
                let contentPath = json[requestedUUID];
                window.location.href = relativeContentDirectory + "/" + contentPath;
            } else {
                document.body.innerText = "the request for a file with a uuid of : " + requestedUUID + " doesn't exist."
            }
        });

}
