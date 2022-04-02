# JMS Pico TKL
## Raspberry Pi Pico powered by CircuitPython and KMK
![JMS-Pico-TKL](/img/finished1.jpg)
Designed and built by: Justine Smithies - [Twitter](https://twitter.com/JustineSmithies) - [GitHub](https://github.com/JustineSmithies)

## **BOM**
|Item                                       |Count|Example|
|:---                                       |:---:|:---:|
|Micro 5Pin Male to USB 2.0 A Female With Screw Panel Mount Cable |1|[Link](https://www.ebay.co.uk/itm/231984473033?hash=item36035a23c9:g:ppYAAOSweBFaqoEh)|
|Raspberry Pi Pico   |1|[Link](https://thepihut.com/collections/pico/products/raspberry-pi-pico)|
|0.96" SSD1306 128x64 Blue |1|[Link](https://www.ebay.co.uk/itm/313603433645?hash=item490438a4ad:g:7cIAAOSwFxlgFY5O)|
|1N4148 Diodes |100|[Link](https://www.ebay.co.uk/itm/313646674409?_trkparms=ispr%3D1&hash=item4906cc71e9:g:kZ8AAOSwxhNhIR6I&amdata=enc%3AAQAGAAAA4HNlZhtmMFCOq5AkzQH0g1bp9XaWKNkLGLOiWFiZxlmCq9DjLAMrg2mvwAyB2RHHrE3dDniqW%2BobKu4v26C3tfEyxvQ2PFxOeH2b29ldf5OfLvKByZQTxMN6oRU2uo9crlDv12TqKz3%2Fgx8%2Bp7mJj1xhxXUTjohUxtKXcReOvlKYzMl0mm8w2Ee9CNXhOk6dhgVcm%2FXnX7wU%2BQSw8NeLLqB1UowcjkWe20YgPIaIAmb9q9IOY5xcMTRZiXKsU77FcZD4aGHLpsCFzptt7cWOkYZCqHfl4BTQDhImGcBxoyI%2B%7Ctkp%3ABFBMgMuwqf1f)|
|Kailh Box Thick Click Jade |90|[Link](https://mechbox.co.uk/collections/switches-packs-of-10/products/novelkeys-x-kailh-box-thick-click-jade-switch-10-switches?variant=40657871274146)|
|MX Keycaps of your choice but I recommend WASD --> |87|[Link](https://www.wasdkeyboards.com/87-key-custom-cherry-mx-keycap-set.html)|
|Custom made stainless steel plate |1|See the remarks below for info
|Everglide Panda GH60 stablizers |1 pack|[Link](https://www.amazon.co.uk/Everglide-Mounted-Stabilizer-Mechanical-Keyboard/dp/B09C4WRLHK/ref=sr_1_6?crid=B1RT91QW1W2F&keywords=Everglide%2BPanda%2BBlack%2BWhite%2BGold%2BPlated%2BPlate%2BMounted&qid=1648913546&sprefix=everglide%2Bpanda%2Bblack%2Bwhite%2Bgold%2Bplated%2Bplate%2Bmounted%2B%2Caps%2C85&sr=8-6&th=1)|

On top of that you'll be needing:
* Soldering iron
* Solder wire (anything between 0.5mm to 1mm, preferable with lead 'Pb')
* Sharp craft knife or wire stripper for cutting sections of insulation out of the wires
* Shapie marker

### **Remarks**

* My plate was made by using the [Keyboard Layout Editor](http://www.keyboard-layout-editor.com/) to make my layout then copied and pasted the raw data into the [Builder](http://www.builder.swillkb.com/) so that I could then order my custom made stainless steel plate from Lasergist.
* I used wire from cat7 cable to wire the switch matrix and used a sharp craft knife to cut them to length for the rows and the columns. I then placed and marked the sections to have the insultation removed with a shapie marker where they are to be soldered to the switches. Using the knife remove the marked insulation being careful not to cut through the wire. This part can take a while and is quite laborious to be honest so you may want to do this over a few days.

# **Build guide**
### *Setup CircuitPython*

* Follow [this](https://circuitpython.org/board/raspberry_pi_pico/) guide in order to have the latest CircuitPython up and running on your Raspberry Pico. When it's installed correctly after plugin it in you should be able to see an additional drive named CIRCUIT_PYTHON or similar. 
* 
