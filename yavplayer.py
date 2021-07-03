#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import sys

def htmlMaker(vidfilepath, srtfilepath):
    result = createPreamble(vidfilepath)
    result += create1stChunk(vidfilepath)
    with open(srtfilepath, 'r') as f:
        sentence = ''
        for line in f:
            line = line.rstrip()
            if re.match(r'^\d+$', line):
                pass
            else:
                m = re.match(r'^([\d:,]+) --> ([\d:,]+)$', line)
                if m is not None:
                    start = getTime(m.group(1))
                    stop = getTime(m.group(2))
                elif re.match(r'^$', line):
                    result += createText(start, stop, sentence[:-2]) + "\n"
                    sentence = ''
                else:
                    sentence = sentence + line + '<br/>　　'
    return result + POSTAMBLE

def getTime(timeStr):
    m = re.match(r'^(\d+):(\d+):(\d+),(\d+)$', timeStr)
    if m is None:
        m = re.match(r'^(\d+):(\d+):(\d+)$', timeStr)
        millisec = 0
    else:
        millisec = int(m.group(4))
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) + millisec / 1000.0

##########################
# HTML template area
##########################

# PREAMBLE
def createPreamble(vidfilepath):
    return """\
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>""" + vidfilepath + """\
</title>
    <link href="./style.css" rel="stylesheet" type="text/css">
  </head>
  <body>
"""

# VIDEO ELEMENT PART
def create1stChunk(videosource):
  return """\
    <div class="split-item split-left">
      <div class="split-left__inner">
        <video id="video01" autoplay src="./""" + videosource + '"' + """\
 width="400"></video><br/>
      <input type="button" id="rewind1secButton" value="Rewind 1 sec." onclick="rewind1sec()"/>
      <input type="button" id="continueButton" value="Play" onclick="continuePlaying()"/>
      <input type="button" id="stopButton" value="Stop" onclick="stopPlaying()"/>
      Vol:<input id="volSlider" type="range" value="100" min="0" max="100" oninput="volume()"/><br/>
      Start point:<select id="startPointAdjuster"/>
        <option value="-3">-3 sec.</option>
        <option value="-2.5">-2.5 sec.</option>
        <option value="-2">-2 sec.</option>
        <option value="-1.5">-1.5 sec.</option>
        <option value="-1">-1 sec.</option>
        <option value="-0.5">-0.5 sec.</option>
        <option value="0" selected>0 sec.</option>
        <option value="0.5">0.5 sec.</option>
        <option value="1">1 sec.</option>
        <option value="1.5">1.5 sec.</option>
        <option value="2">2 sec.</option>
        <option value="2.5">2.5 sec.</option>
        <option value="3">3 sec.</option>
      </select>
      Stop point:<select id="stopPointAdjuster"/>
        <option value="-3">-3 sec.</option>
        <option value="-2.5">-2.5 sec.</option>
        <option value="-2">-2 sec.</option>
        <option value="-1.5">-1.5 sec.</option>
        <option value="-1">-1 sec.</option>
        <option value="-0.5">-0.5 sec.</option>
        <option value="0" selected>0 sec.</option>
        <option value="0.5">0.5 sec.</option>
        <option value="1">1 sec.</option>
        <option value="1.5">1.5 sec.</option>
        <option value="2">2 sec.</option>
        <option value="2.5">2.5 sec.</option>
        <option value="3">3 sec.</option>
      </select>
      <br/>
      Speed:<select id="speedSelector" onchange="speedSet();"/>
        <option value="0.25">0.25</option>
        <option value="0.50">0.50</option>
        <option value="0.75">0.75</option>
        <option value="1.00" selected>1.00</option>
        <option value="1.25">1.25</option>
        <option value="1.50">1.50</option>
        <option value="1.75">1.75</option>
        <option value="2.00">2.00</option>
      </select>
      </div><!--split-left__inner-->
    </div><!--split-item split-left-->
    <div class="split-item split-right">
      <div class="split-right__inner">
""";

# ANCHOR PART
def createText(start, stop, text):
    return '      <a href="javascript:playAportion(' + str(start) + ',' + str(stop) + ')">🔊 ' + text + '</a>'


POSTAMBLE = """\
      </div><!--split-right__inner-->
    </div><!--split-item split-right-->
  </div><!--split-->
    <script>
      const vplayer = document.getElementById("video01");
      const volSlider = document.getElementById("volSlider");
      const continueButton = document.getElementById("continueButton");
      const stopButton = document.getElementById("stopButton");
      const speedSelector = document.getElementById("speedSelector");
      const startPointAdjuster = document.getElementById("startPointAdjuster");
      const stopPointAdjuster = document.getElementById("stopPointAdjuster");

      stopButton.disabled = true;

      function _inPlay(flag) {
        if (flag) {
          continueButton.disabled = true;
          stopButton.disabled = false;
        } else {
          continueButton.disabled = false;
          stopButton.disabled = true;
        }
      }

      function playAportion(start, stop) {
        vplayer.currentTime = Number(start) + Number(startPointAdjuster.value);
        vplayer.ontimeupdate = function() {
          if (vplayer.currentTime >= Number(stop) + Number(stopPointAdjuster.value)) {
            vplayer.pause();
            vplayer.ontimeupdate = null;
            _inPlay(false);
            
          }
        };
        vplayer.play();
        _inPlay(true);
      }
      function rewind1sec() {
        vplayer.currentTime -= 1.0;
      }
      function continuePlaying() {
        vplayer.play();
        _inPlay(true);
      }
      function stopPlaying() {
        vplayer.pause();
        vplayer.ontimeupdate = null;
        _inPlay(false);
      }
      function volume() {
        vplayer.volume = volSlider.value / 100.0;
      }
      function speedSet() {
        vplayer.playbackRate = Number(speedSelector.value);
      }
    </script>
</body></html>
"""

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


from sys import argv

if len(argv) != 3:
    eprint('yavplayer: Usage\n  videofilename srtfilename')
else:
    outfilename = re.sub(r'\.[a-z0-9]+$', '', argv[1], re.IGNORECASE) + '.html'
    with open(outfilename, mode='w') as of:
      of.write(htmlMaker(argv[1], argv[2]))

