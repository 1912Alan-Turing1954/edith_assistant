from TTS.api import TTS
import simpleaudio as sa
import os, re

acronyms_dict = {
    # More Electrical Acronyms
    "ACB": "Air Circuit Breaker",
    "DCB": "Distribution Circuit Breaker",
    "CT": "Current Transformer",
    "PT": "Potential Transformer",
    "FET": "Field-Effect Transistor",
    "BJT": "Bipolar Junction Transistor",
    "SCR": "Silicon Controlled Rectifier",
    "IGBT": "Insulated Gate Bipolar Transistor",
    "PID": "Proportional-Integral-Derivative",
    "SPST": "Single-Pole, Single-Throw",
    "DPST": "Double-Pole, Single-Throw",
    "SPDT": "Single-Pole, Double-Throw",
    "DPDT": "Double-Pole, Double-Throw",
    "RJ45": "Registered Jack 45",
    "NVRAM": "Non-Volatile Random-Access Memory",
    "UPS": "Uninterruptible Power Supply",
    "PDU": "Power Distribution Unit",
    "GFCI": "Ground Fault Circuit Interrupter",
    "EMC": "Electromagnetic Compatibility",
    "EMI": "Electromagnetic Interference",
    "PLC": "Programmable Logic Controller",
    "DMM": "Digital Multimeter",
    "CCTV": "Closed-Circuit Television",
    "NFC": "Near Field Communication",
    "PID": "Proportional-Integral-Derivative",
    "RMS": "Root Mean Square",
    "THD": "Total Harmonic Distortion",
    "VA": "Volt-Ampere",
    "VAR": "Volt-Ampere Reactive",
    "PF": "Power Factor",
    "kV": "Kilovolt",
    "mV": "Millivolt",
    "Amp": "Ampere",
    "Hz": "Hertz",
    "Ohm": "Ohm",
    "Watt": "Watt",
    "Farad": "Farad",
    "Henry": "Henry",
    "Joule": "Joule",
    "Coulomb": "Coulomb",
    "Tesla": "Tesla",
    "Siemens": "Siemens",
    "Hertz": "Hertz",
    "Volt": "Volt",
    "Ohm's Law": "Ohm's Law",
    "Kirchhoff's Laws": "Kirchhoff's Laws",
    "Electric Field": "Electric Field",
    "Magnetic Field": "Magnetic Field",
    "Inductance": "Inductance",
    "Capacitance": "Capacitance",
    "Resistor": "Resistor",
    "Diode": "Diode",
    "Transistor": "Transistor",
    "Amplifier": "Amplifier",
    "Oscillator": "Oscillator",
    "Relay": "Relay",
    "Fuse": "Fuse",
    "Generator": "Generator",
    "Motor": "Motor",
    "Transformer": "Transformer",
    "Circuit": "Circuit",
    "Conductor": "Conductor",
    "Insulator": "Insulator",
    "Ground": "Ground",
    "Electrostatics": "Electrostatics",
    "Electromagnetism": "Electromagnetism",
    "Circuit Breaker": "Circuit Breaker",
    "Electrical Panel": "Electrical Panel",
    "Voltage Regulator": "Voltage Regulator",
    "Wiring Diagram": "Wiring Diagram",
    "Short Circuit": "Short Circuit",
    "Overload": "Overload",
    "Circuit Diagram": "Circuit Diagram",
    "Ohmmeter": "Ohmmeter",
    "Voltmeter": "Voltmeter",
    "Ammeter": "Ammeter",
    "Wattmeter": "Wattmeter",
    "Grounding": "Grounding",
    "Electrical Shock": "Electrical Shock",
    "DC": "Direct Current",
    "V": "Volt (Voltage)",
    "A": "Ampere (Current)",
    "Ω": "Ohm (Resistance)",
    "W": "Watt (Power)",
    "F": "Farad (Capacitance)",
    "H": "Henry (Inductance)",
    "C": "Coulomb (Electric Charge)",
    "T": "Tesla (Magnetic Flux Density)",
    "S": "Siemens (Conductance)",
    "Hz": "Hertz (Frequency)",
    "VA": "Volt-Ampere (Apparent Power)",
    "VAR": "Volt-Ampere Reactive (Reactive Power)",
    "PF": "Power Factor",
    "kV": "Kilovolt",
    "mV": "Millivolt",
    "μV": "Microvolt",
    "nV": "Nanovolt",
    "pV": "Picovolt",
    "kA": "Kiloampere",
    "mA": "Milliampere",
    "μA": "Microampere",
    "nA": "Nanoampere",
    "pA": "Picoampere",
    "Ωm": "Ohm-Meter (Resistance x Length)",
    "W/m²": "Watt per Square Meter (Irradiance)",
    "J": "Joule (Energy)",
    "eV": "Electronvolt (Energy)",
    "GΩ": "Gigaohm",
    "MΩ": "Megaohm",
    "kΩ": "Kiloohm",
    "mΩ": "Milliohm",
    "μΩ": "Microohm",
    "nΩ": "Nanoohm",
    "pΩ": "Picoohm",
    "nF": "Nanofarad",
    "pF": "Picofarad",
    "fF": "Femtofarad",
    "μH": "Microhenry",
    "nH": "Nanohenry",
    "pH": "Picohenry",
    "Tm²": "Tesla Square Meter (Magnetic Flux)",
    "GΩm": "Gigaohm-Meter",
    "MΩm": "Megaohm-Meter",
    "kΩm": "Kiloohm-Meter",
    "mΩm": "Milliohm-Meter",
    "μΩm": "Microohm-Meter",
    "nΩm": "Nanoohm-Meter",
    "pΩm": "Picoohm-Meter",
}


def replace_acronyms(text, acronyms_dict):
    # Find all words in the text
    words = text.split()

    # Initialize an empty list to store the modified words
    modified_words = []

    for word in words:
        # Remove any non-alphanumeric characters from the word
        clean_word = re.sub(r"[^a-zA-Z0-9]", "", word)

        # Check if the clean_word is an acronym in the dictionary
        if clean_word.upper() in acronyms_dict:
            # Replace the acronym with its full form
            full_form = acronyms_dict[clean_word.upper()]
            modified_words.append(full_form)
        else:
            modified_words.append(word)

    # Reconstruct the modified text
    modified_text = " ".join(modified_words)

    return modified_text


def text_to_speech(text):
    # Replace acronyms in the text with their full forms
    text = replace_acronyms(text, acronyms_dict)

    decimal_pattern = r"\d+\.\d+"

    # Find all occurrences of the pattern in the text
    decimal_matches = re.findall(decimal_pattern, text)

    # Replace decimal points with "point"
    for match in decimal_matches:
        text = text.replace(
            match, match.replace(".", " point "), 1
        )  # Replace only the first occurrence

    tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)
    tts.tts_to_file(text, file_path="tts_/output.wav")

    # Run TTS
    filename = "tts_/output.wav"
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove("tts_/output.wav")
