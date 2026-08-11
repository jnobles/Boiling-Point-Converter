const form = document.getElementById("calculator")

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const referencePressure = document.getElementById("reference-pressure").value;
    const referenceTemperature = document.getElementById("reference-temperature").value;
    const mode = form.elements["solver-mode"].value;
    const atValue = document.getElementById("at-value").value;

    console.log({
        referencePressure,
        referenceTemperature,
        mode,
        atValue,
    });
});

async function main(){
        let pyodide = await loadPyodide();
        console.log(pyodide.runPython("1 + 2"));
      }
      main();