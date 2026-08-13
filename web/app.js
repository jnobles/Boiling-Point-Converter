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
        resultOutput.textContent = formatResult(event.data.result);
    }
    if (event.data.type === "dataTable") {
        const dataTable = JSON.parse(event.data.json);
        const dhVapList = document.getElementById("dh-vap-options");
        for (const item of dataTable) {
            const listItem = document.createElement("li");
            const option = document.createElement("input");
            option.id = `dh-vap-${item.compound.replaceAll(" ", "-")}`;
            option.type = "radio";
            option.name = "dh-vap";
            option.value = item.dh_vap_kj_per_mol;

            const label = document.createElement("label");
            label.htmlFor = option.id;
            label.textContent = item.compound;

            listItem.appendChild(option);
            listItem.appendChild(label);

            dhVapList.appendChild(listItem);
        }
    }
    if (event.data.type === "error") {
        const resultOutput = document.getElementById("result");
        resultOutput.textContent = event.data.message;
    }
});

const form = document.getElementById("calculator");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const referencePressure = document.getElementById("reference-pressure").valueAsNumber;
    const referenceTemperature = document.getElementById("reference-temperature").valueAsNumber;
    const mode = form.elements["solver-mode"].value;
    const atValue = document.getElementById("at-value").valueAsNumber;
    const dhVap = document.getElementById("dh-vap").valueAsNumber;

    worker.postMessage({
        type: "calculate",
        p1: referencePressure,
        t1: referenceTemperature,
        mode: mode,
        atValue: atValue,
        dhVap: dhVap,
    });
});

const fieldsetDhVap = document.getElementById("heat-of-vaporization");
const dhVap = document.getElementById("dh-vap");

fieldsetDhVap.addEventListener("change", (event) => {
    if (event.target.type === "radio") {
        dhVap.value = event.target.value;
    }
});

dhVap.addEventListener("input", () => {
    if (dhVap.value !== "") {
        for (const radio of form.elements["dh-vap"]) {
            radio.checked = false;
        }
    }
})

function formatResult(result) {
    let p2;
    let t2;
    if (result.mode === "pressure") {
        p2 = result.atValue;
        t2 = result.result;
    } else if (result.mode === "temperature") {
        t2 = result.atValue;
        p2 = result.result;
    }
    return (
        `Using Heat of Vaporization: ${result.dhVap.toFixed(2)} kJ/mol,

Pressure: ${result.p1.toFixed(2)} torr
Boiling Point: ${result.t1.toFixed(2)} °C

Equates to,

Pressure: ${p2.toFixed(2)} torr
Boiling Point: ${t2.toFixed(2)} °C`
    )
}

const atValueUnit = document.getElementById("at-value-unit");
const fieldsetAtValueUnit = document.getElementById("target-value");

fieldsetAtValueUnit.addEventListener("change", (event) => {
    if (event.target.type === "radio") {
        if (event.target.value === "pressure") {
            atValueUnit.textContent = "torr";
        } else if (event.target.value === "temperature") {
            atValueUnit.textContent = "°C";
        }
    }
});