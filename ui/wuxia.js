function callApi(templateType) {
  const apiGatewayUrl = document.getElementById('apiGatewayUrl').value;
  const contentId = `${templateType}-content`;
  const temperatureId = `${templateType}-temperature`;
  const topPId = `${templateType}-topP`;
  
  const modelId = document.getElementById('modelSelector').value;
  const content = document.getElementById(contentId).value;
  const temperature = parseFloat(document.getElementById(temperatureId).value);
  const topP = parseFloat(document.getElementById(topPId).value);

  let templateId;
  switch (templateType) {
    case 'generate': templateId = 'generate_code'; break;
    case 'translate': templateId = 'translate_code'; break;
    case 'analyze': templateId = 'analyze_code'; break;
    case 'ask': templateId = 'ask_question'; break;
    default: templateId = '';
  }

  const requestBody = { modelId, templateId, content, temperature, topP };

  fetch(apiGatewayUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody)
  })
  .then(response => response.text())
  .then(outputText => {
	  document.getElementById('output').value = outputText;
  })
  .catch(error => {
    console.error("Error:", error);
    alert("An error occurred: " + error);
  });
}

const tabLinks = document.querySelectorAll('.tabs li a');
const tabPanes = document.querySelectorAll('.tab-pane');

tabLinks.forEach(link => {
  link.addEventListener('click', e => {
	e.preventDefault();

	tabLinks.forEach(link => link.parentElement.classList.remove('is-active'));
	tabPanes.forEach(pane => pane.classList.remove('is-active'));

	document.getElementById('output').value = '';

	const targetTab = e.target.getAttribute('data-tab');
	const targetPane = document.querySelector(`.tab-pane[data-pane="${targetTab}"]`);

	e.target.parentElement.classList.add('is-active');
	targetPane.classList.add('is-active');
  });
});

document.querySelectorAll('.slider').forEach(slider => {
  // On slider input
  slider.addEventListener('input', function () {
	const labelElement = this.closest('.field')?.querySelector('label');
	const label = this.id.includes('temperature') ? 'Temperature' : 'Top P';
	if (labelElement) {
	  labelElement.textContent = `${label}: ${parseFloat(this.value).toFixed(2)}`;
	}
  });

  // Initialization on page load
  const labelElement = slider.closest('.field')?.querySelector('label');
  const label = slider.id.includes('temperature') ? 'Temperature' : 'Top P';
  let value = parseFloat(slider.value);
  if (isNaN(value)) {
	value = slider.id.includes('temperature') ? 0.7 : 0.95;
  }
  if (labelElement) {
	labelElement.textContent = `${label}: ${value.toFixed(2)}`;
  }
});
