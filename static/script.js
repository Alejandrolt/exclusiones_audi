document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const fileNameSpan = document.getElementById("file-name");
  const form = document.querySelector("form");
  const spinner = document.getElementById("spinner");
  const submitButton = form.querySelector("button");

  const MAX_FILE_SIZE_MB = 5;

  // Mostrar nombre del archivo
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    fileNameSpan.textContent = file ? file.name : "Ningún archivo seleccionado";
  });

  // Validar y enviar el formulario
  form.addEventListener("submit", (e) => {
    const file = fileInput.files[0];

    // Validar existencia del archivo
    if (!file) {
      alert("Por favor selecciona un archivo.");
      e.preventDefault();
      return;
    }

    // Validar tipo MIME (puedes ajustar si aceptas más formatos)
    if (!file.name.endsWith(".xlsx")) {
      alert("El archivo debe tener extensión .xlsx");
      e.preventDefault();
      return;
    }

    // // Validar tamaño (en MB)
    // const sizeMB = file.size / (1024 * 1024);
    // if (sizeMB > MAX_FILE_SIZE_MB) {
    //   alert(`El archivo excede los ${MAX_FILE_SIZE_MB} MB permitidos.`);
    //   e.preventDefault();
    //   return;
    // }

    // Si todo está bien, desactivar botón y mostrar spinner
    submitButton.disabled = true;
    submitButton.textContent = "Procesando...";
    spinner.style.display = "block";
  });
});
