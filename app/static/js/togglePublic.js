

document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.getElementById('checkedToggle');
    const campaignId = checkbox.getAttribute("campaign-id");
    let routeURL;
    checkbox.addEventListener('change', function() {
      const isChecked = checkbox.checked;
      const label = checkbox.nextElementSibling;
      const paragraph = label.querySelector('p');
      paragraph.textContent = isChecked ? 'Public' : 'Private';
      routeURL = '/togglePublic/' + campaignId;

      fetch(routeURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ checked: isChecked })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
      });
    });
  });