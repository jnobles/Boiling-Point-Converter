const worker = new Worker(
    "./pyodide-worker.js",
    {type: "module"},
);

worker.addEventListener("message", (event) => {
    if (event.data.type === "ready") {
        const calculateButton = document.getElementById("calculate");
        calculateButton.disabled = false;
        calculateButton.textContent = "Calculate";
    }
    if (event.data.type === "result") {
        const resultOutput = document.getElementById("result");
        resultOutput.textContent = event.data.result;
    }
    if (event.data.type === "dataTable") {
        const dataTable = JSON.parse(event.data.json);
        const fieldset = document.getElementById("heat-of-vaporization");
        for (const item of dataTable) {
            const option = document.createElement("input");
            option.id = `dh-vap-${item.compound.replaceAll(" ", "-")}`;
            option.type = "radio";
            option.name = "dh-vap";
            option.value = item.dh_vap_kj_per_mol;

            const label = document.createElement("label");
            label.htmlFor = option.id;
            label.textContent = item.compound;

            fieldset.appendChild(option);
            fieldset.appendChild(label);
        }
    }
});

const form = document.getElementById("calculator");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const referencePressure = Number(document.getElementById("reference-pressure").value);
    const referenceTemperature = Number(document.getElementById("reference-temperature").value);
    const mode = form.elements["solver-mode"].value;
    const atValue = Number(document.getElementById("at-value").value);
    const dhVap = Number(document.getElementById("dh-vap").value);

    worker.postMessage({
        type: "calculate",
        p1: referencePressure,
        t1: referenceTemperature,
        mode: mode,
        atValue: atValue,
        dhVap: dhVap,
    });
});

const fieldset = document.getElementById("heat-of-vaporization");
const dhVap = document.getElementById("dh-vap");

fieldset.addEventListener("change", (event) => {
    if (event.target.type === "radio") {
        dhVap.value = event.target.value === "custom"
            ? ""
            : event.target.value
    }
});