import {
    loadPyodide
} from "https://cdn.jsdelivr.net/pyodide/v314.0.4/full/pyodide.mjs"

let pyodide;

async function initializePyodide() {
    pyodide = await loadPyodide();

    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install("./boiling_point_converter-1.0.1-py3-none-any.whl");
    pyodide.runPython(`from boiling_point_converter.core import perform_calculation`)
    console.log("Pyodide ready");
    postMessage({
        type: "ready",
    });
}

function heats_of_vaporization() {
    const heats_of_vaporization = pyodide.runPython(`
        import json
        from dataclasses import asdict
        from boiling_point_converter.core.molar_heat_of_vaporization import REFERENCE_HEATS_OF_VAPORIZATION as data_table
        json.dumps([asdict(item) for item in data_table])
    `);
    postMessage({
        type: "dataTable",
        json: heats_of_vaporization,
    });
}

function calculate(data) {
    pyodide.globals.set("p1", data.p1);
    pyodide.globals.set("t1", data.t1);
    pyodide.globals.set("mode", data.mode);
    pyodide.globals.set("at_value", data.atValue);
    pyodide.globals.set("dh_vap", data.dhVap);

    try {
        const result = pyodide.runPython(`
        perform_calculation(
            mode=mode,
            p1=p1,
            t1=t1,
            at_value=at_value,
            dh_vap=dh_vap,
            )
        `);

        postMessage({
            type: "result",
            result: {
                mode: data.mode,
                p1: data.p1,
                t1: data.t1,
                atValue: data.atValue,
                dhVap: data.dhVap,
                result: result,
            },
        });
    } catch (error) {
        postMessage({
            type: "error",
            message: error.toString(),
        });
    }

}

self.addEventListener("message", (event) => {
    if (event.data.type === "calculate") {
        calculate(event.data);
    }
});

await initializePyodide();
heats_of_vaporization();