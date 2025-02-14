import fluidsynth
import rtmidi
import os
from flask import Flask, render_template, request, jsonify
from multiprocessing import Process, Queue, Value

qVal = None
app = Flask(__name__)

def checkQueue():
    if not qVal.empty():
        qData = qVal.get()
        if qData[0] == "reverb":
            fs.set_reverb_level(qData[1])
        if qData[0] == "damp":
            print("DAMP")
            fs.set_reverb_damp(qData[1])
        if qData[0] == "width":
            fs.set_reverb_width(qData[1])
        if qData[0] == "size":
            fs.set_reverb_roomsize(qData[1])

def loop(midiin):
    while True:
        checkQueue()
        m = midiin.getMessage(0) # some timeout in ms
        if m and m.isNoteOn():
            fs.noteon(0, m.getNoteNumber(), m.getVelocity())
        if m and m.isNoteOff():
            fs.noteoff(0, m.getNoteNumber())

def openMidiInput():
    midiin = rtmidi.RtMidiIn()
    ports = range(midiin.getPortCount())
    if ports:
        for i in ports:
            print(midiin.getPortName(i))
            if "MPK249" in midiin.getPortName(i):
                midiin.openPort(i)
                break
        loop(midiin)
    else:
        print('NO MIDI INPUT PORTS!')

def buildFlaskApp(q):
    global qVal
    qVal = q
    app.run(debug=False)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/knobChanged', methods=["POST"])
def updateParameter():
    msg = ""
    global qVal
    if request.json['knob'] == "r-wet-knob":
        qVal.put(["reverb", 1.0 - float(request.json["value"])/100.0])
    if request.json['knob'] == "r-damp-knob":
        qVal.put(["damp", 1.0 - float(request.json["value"])/100.0])
    if request.json['knob'] == "r-width-knob":
        qVal.put(["width", 100.0 - float(request.json["value"])])
    if request.json['knob'] == "r-size-knob":
        qVal.put(["size", 1.0 - float(request.json["value"])/100.0])
    return jsonify(msg)

if __name__ == "__main__":
    fs = fluidsynth.Synth()
    fs.start(driver='dsound')
    sfid = fs.sfload('./DIYtron.sf2')
    fs.program_select(0, sfid, 0, 0)
    fs.set_reverb(roomsize=0.5, damping=0.5, width=50.0, level=0)
    qVal = Queue()
    p1 = Process(target=buildFlaskApp, args=(qVal,))
    p1.start()
    openMidiInput()

# def print_message(midi):
#     if midi.isNoteOn():
#         print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
#     elif midi.isNoteOff():
#         print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
#     elif midi.isController():
#         print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
