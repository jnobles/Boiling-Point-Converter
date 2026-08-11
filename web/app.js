let pyodideReady;

async function initializePyodide() {
    console.time("Pyodide initialization");

    console.time("loadPyodide");
    const pyodide = await loadPyodide();
    console.timeEnd("loadPyodide");

    console.time("load micropip");
    await pyodide.loadPackage("micropip");
    console.timeEnd("load micropip");

    console.time("install calculator");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("./boiling_point_converter-1.0.1-py3-none-any.whl");
    console.timeEnd("install calculator");

    console.log("Pyodide ready");
    console.timeEnd("Pyodide initialization")
    return pyodide
}

async function main() {
    const form = document.getElementById("calculator");
    const calculateButton = document.getElementById("calculate");

    pyodideReady = initializePyodide();
    pyodideReady.then(() => {
        calculateButton.disabled = false;
        calculateButton.textContent = "Calculate";
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const pyodide = await pyodideReady;

        const referencePressure = Number(document.getElementById("reference-pressure").value);
        const referenceTemperature = Number(document.getElementById("reference-temperature").value);
        const mode = form.elements["solver-mode"].value;
        const atValue = Number(document.getElementById("at-value").value);

        pyodide.globals.set("p1", referencePressure);
        pyodide.globals.set("t1", referenceTemperature);
        pyodide.globals.set("at_value", atValue);
        pyodide.globals.set("mode", mode)
        pyodide.globals.set("dh_vap", 40);

        const result = pyodide.runPython(`
            from boiling_point_converter.core import perform_calculation
            perform_calculation(mode, p1, t1, at_value, dh_vap)
        `);
        console.log(result);
    });
}

 main();