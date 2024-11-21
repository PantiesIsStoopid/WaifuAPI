function fetchImage() {
  const tags = document.getElementById('tags').value;
  const height = document.getElementById('height').value;

  // Show loading status
  document.getElementById('status').innerText = 'Fetching image...';

  // Prepare the request URL
  const apiUrl = 'https://api.waifu.im/search'; // Replace with the actual API endpoint URL
  const params = {
    included_tags: tags.split(','), // Split input tags into an array
    height: `>=${height}`,
  };

  const queryParams = new URLSearchParams();

  // Construct the query string
  for (const key in params) {
    if (Array.isArray(params[key])) {
      params[key].forEach((value) => {
        queryParams.append(key, value);
      });
    } else {
      queryParams.set(key, params[key]);
    }
  }

  const requestUrl = `${apiUrl}?${queryParams.toString()}`;

  // Fetch the image data from the API
  fetch(requestUrl)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Request failed with status code: ' + response.status);
      }
    })
    .then((data) => {
      if (data.images && data.images.length > 0) {
        const imageUrl = data.images[0].url; // Get the URL of the first image
        const img = document.createElement('img');
        img.src = imageUrl;

        // Display the image
        document.getElementById('image-container').innerHTML = ''; // Clear previous image
        document.getElementById('image-container').appendChild(img);

        // Show success message
        document.getElementById('status').innerText =
          'Image fetched successfully!';
      } else {
        document.getElementById('status').innerText =
          'No images found for the given tags and height.';
      }
    })
    .catch((error) => {
      document.getElementById('status').innerText = 'Error fetching image.';
      console.error('An error occurred:', error.message);
    });
}