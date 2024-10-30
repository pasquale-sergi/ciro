import { createStore } from 'vuex';

const store = createStore({
    state: {
        updates: [{
            title: "Update 1: Initial Design",
            content: `
          Started sketching the initial design and layout for the robotic arm,
          focusing on achieving six degrees of freedom.
          <br><br>
          I'm taking inspiration from various existing 3D models. The goal, as
          mentioned in the overview, is not the arm design itself but the
          functionality and machine learning applications. Additionally, I
          believe 3D modeling requires a significant amount of time, which,
          unfortunately, I don't have right now.
          <br><br>
          I'm aiming for a medium-sized arm, ideally something that can reach a
          maximum extension of 30 cm. The reason is that I want it to be useful
          for a precise task that I haven't determined yet, and I want to ensure
          it will be as flexible as possible in terms of measurements.
          <br><br>
        `,
            tag: "printing"
        },
        {
            title: "Update 2: Component Selection",
            content: `
          I conducted different research to find the best components to achieve
          the goal while keeping an eye on the price, of course. The budget for
          the hardware is approximately 250 euros, which is sufficient to make
          the arm capable of precise and speed-controlled movement.
          <br><br>
          The current blueprint predicts a total of 4 stepper motors and 2
          servos. I decided to go with stepper motors for the majority because
          they are easier to use, more precise, and better at maintaining high
          torque when a heavy load is applied. However, both options present
          their pros and cons, so I suggest doing your own research and deciding
          based on your goals.
          <br><br>
          The motors will be directly controlled by the Arduino, leaving the
          Raspberry Pi free for the AI models.
          <br><br>
          The gripper is currently a question mark; the plan is to install a
          stepper motor at the end of the arm pointing forward, making the end
        `,
            tag: "hardware"

        },
        {
            title: "Update 3: Start working on the first model",
            content: `
          While waiting for hardware parts to be delivered and 3D parts to be
          printed, I'm starting to work on the first model, which will be the
          wake-word detection one. The trigger word will be "Ciro," as I called
          it. Ciro is a famous and common Neapolitan name, and as an Italian, I
          thought it was the best way to give that touch of patriotism.
          <br><br>
          The first thing I need is data; at this point, I learned that data is
          arguably the most important piece of the entire structure. The plan is
          to ask all my friends and parents for voice clips with the word "Ciro"
          in them—ideally different clips with various tones and speeds to make
          the model more flexible and robust. I give myself 3 days for this
          task.
          <br><br>
          Update of the Update - while collecting the data, I realized I have
          much fewer friends than I thought. I asked 5 samples from each friend,
          but after two days, I have a little more than 100 clips, which are not
          sufficient for a decent model. So, I decided to go with just my voice;
          after all, the arm will stay in my room, and I'm likely the only human
          interacting with it. Plus, I can always keep collecting data and
          retrain the model in the future. Also, another potential issue that
          I'm facing—and that I'm glad I discovered before recording a thousand
          samples—is that the data is being collected through my iPhone while
          the arm will listen to speech with a totally different device. I still
          don't know much, but I think such different devices will make it much
          harder for the model to detect the word. Also, I was planning to
          record some data with the same procedure for the speech-to-text model,
          too, so that would have been much worse.
          <br><br>
          What now? I have to wait for the microphone and the ESP32 so I can
          connect everything and start collecting data with the new microphone.
          Of course, I won't delete the samples I already have; I will integrate
          them.
          <br><br>
          In the meantime, I think it's a good idea to start implementing the
          code for the model so that I can feel confident in the environment,
          considering I'm totally new to this. I want to clarify that I already
          have some knowledge of Python, though.
          <br><br>
          The data I'm using is composed of 100 positive samples containing the
          word "Ciro" and 150 negative ones.
          <br><br>
          From what I've learned so far, the procedure is pretty
          straightforward:
          <br><br>
          <div class="procedure">
            <div class="procedure-step">Audio samples ➜ Generate spectrograms</div>
            <div class="procedure-step">➜ Assign labels (1 for positive and 0 for negative)</div>
            <div class="procedure-step">➜ Split the data into training set and validation set</div>
            <div class="procedure-step">➜ Pass the training set to the model</div>
            <div class="procedure-step">➜ Test with the validation set</div>
          </div>
          <br><br>
          <div class="model-implementation">
            <p>
              Here you can find the code of the model, if you want to see how I do
              it. This is the blueprint so the model trained with the 100 samples,
              it looks like it works but still surely needs some improvements.
            </p>
            <div class="github-link">
                <a href="https://github.com/pasquale-sergi/ciro/tree/main/model1-wake-word">wake word model</a>
            </div>
          </div>
        `,
            tag: "ai"
        },
        {
            title: "Update 4: Skill issues",
            content: `
          I received the Raspberry Pi 5, and let me just say, it’s been a bit of a pain. I thought I’d install Ubuntu and be done with it, but a firmware error stopped me in my tracks. I assumed the issue was with the SD card, even though it was brand new, so I swapped it out with two others. Same error. I erased both SD cards and decided to try Raspberry Pi OS, which is recommended by the Raspberry Pi Imager. The writing process went fine, but there was an error during verification. I was almost ready to give up, but I decided to try one last thing. I installed the OS on a flash drive, plugged it into the Pi, and thank God—it worked.
          <br><br>
          However, during installation, I got a new warning: “The device needs 5V, and the current power supply doesn’t meet this requirement.” I was confused because I bought a power supply specifically for the Raspberry Pi, even though it was labeled for the Raspberry Pi 4. I figured it would be compatible, but apparently, the 5V 15W charger isn’t enough—the new Pi needs 27W.
          <br><br>
          (Also, it’s crazy how you need five different power supplies, and they only give you the Raspberry Pi itself.)
          <br><br>
          Anyway, I’m almost happy with it, although it’s running pretty laggy. The browser took a solid five minutes to open, and I’m not sure if that’s because I’m still waiting on the cooler to arrive. I’ve seen videos where people talk about it being a real PC with real power, able to handle multiple monitors and various applications. Right now, I’m not even sure it can handle my wake-word detection model.
          <br><br>
          Oh, and I did my first soldering while setting this up. Of course, it didn’t go well, and worse, I messed up the Adafruit microphone I was planning to use to record my data. It’s so bad that I’ll have to show you!
          <div class="sold-img">
            <img class="soldering-img" src="/bad-soldering2.png" />
          </div>
        `,
            tag: "hardware"
        },


        {
            title: "Update 5: A win is a win",
            content: `So, the last update was me soldering the mic so poorly that I broke it. A week has passed, and in the meantime, I ordered a new mic and upgraded my setup with a better soldering station—because, of course, the issue was the station, not my skill level. <br><br>
        
        While waiting for the delivery, I thought, "Let's wire the mic to the Pi 5 anyway, just to get comfortable with the pins." Smart, right? Well, even smarter would have been to test the broken mic *before* buying a new one! To my surprise, the mic was actually working. I wrote a quick Python script to test it with some audio clips, and it picked up sound just fine.<br><br>
        
        The audio is a bit distorted at the beginning and end of each clip, but I believe that's just the mic itself, so I've decided to leave it as it is. I'll share the script below for those curious to see it.<br><br>I also discovered the Raspberry Pi was slow because, due to my malfunctioning SD card, I had installed the OS on a USB drive. This caused limited read and write speeds. My bad, Raspi!<br><br>
        
        Anyway, after ordering a new SD card and reinstalling the OS, the Pi’s performance has vastly improved. I set up the camera and took some test photos to ensure everything worked. This sounds easy and cool, but the reality took me an entire day. To start, the Pi 5 has a 9-pin connector, while the camera module uses a 12-pin. <br><br>
        
        Finding the right adapter was a pain in the butt, especially since the Pi Camera Module V2 is recommended for the Pi 5. I almost gave up and was about to order the Module V3 (a steep 50 euros), but then a cheaper 5MP camera with a 9-pin connector appeared in my Amazon feed for just 12 euros. So, I paid 12 euros essentially for the right connector—but hey, a win is a win.<br><br>
        
        After attaching everything and installing the necessary libraries, I finally got the camera preview to work. However, the focus was terrible. I almost felt like crying, so I reached out to ChatGPT with, "My new camera module V2 focus is so bad I’m about to cry. How will I ever train my model on chess pieces with this?" And, as always, she came to the rescue, explaining that the camera lens has a small adjustable ring for focus.<br><br>
        
        Now, I have both the camera and mic working. I tested the camera by taking some photos of my coffee cup using a simple Python script.`,
            tag: "hardware"
        },

        {
            title: "Update 6: The art of 3d modeling",
            content: `What about the printing? I know this is going to be the biggest challenge because I chose to find a model and "adapt it." I printed some pieces, but every time, something is off. I'm starting to think that the models you find online are not meant for real production because most of the time, the measurements are incorrect, or pieces simply aren't compatible when you try to assemble them.<br><br>
    
    Skill issues? Probably, especially since I could have learned 3D modeling and built my own structure. I'm actually considering it now that the project is coming together. However, I'm also scared of the time this will require. With all these variables, the probability of needing to reprint is higher, which means a lot of time wasted since the printer is so slow.<br><br>
    
    Anyway, I’m currently printing a model I found online that looks almost reasonable. I have some questions, but I'll wait for the printer to finish before doubting it.<br><br>
    
    <div class="link">
Link to the model:    <a class="model-link" href="https://grabcad.com/library/6-axis-robot-arm-4">arm model</a></div><br><br>
    
    It actually looks fine and is compatible with NEMA 17 motors, which are the steppers I plan to use, even though I have some servos planned as well. That's why I mentioned I will adapt it—hopefully without much trouble.`,
            tag: "printing"
        }
        ],

    },

    getters: {
        allUpdates: (state) => state.updates,
        hardwareUpdates: (state) => state.updates.filter(update => update.tag === "hardware"),
        aiUpdates: (state) => state.updates.filter(update => update.tag === "ai"),
        printingUpdates: (state) => state.updates.filter(update => update.tag === "printing")
    }
})
export default store;
