const evtSource = new EventSource("/events");
evtSource.onmessage = (event) => {
    const message = event.data;
    if (message.startsWith("New photo: ")) {
        const filename = message.replace("New photo: ", "");
        const img = document.createElement("img");
        img.src = `/photos/${filename}`;
        document.getElementById("photo-container").appendChild(img);
    }
};
