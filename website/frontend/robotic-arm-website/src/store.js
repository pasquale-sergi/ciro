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
            
            The audio is a bit distorted at the beginning and end of each clip, but I believe that's just the mic itself, so I've decided to leave it as it is. I'll share the script below for those curious to see it.<br><br>I also discovered the Raspberry Pi was slow because, due to my malfunctioning SD card, I had installed the OS on a USB drive. This caused limited read and write speeds. My bad, raspi.br><br>
            
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
        },
        {
            title: "Update 8: Hands on the Object Detection Model",
            content: `I'm starting to work on the object detection model. The initial plan was to train the arm to recognize 3-5 different objects and, through voice commands, have it perform specific actions with them. However, since I haven’t yet thought of a practical task beyond "grab and move," I’ve decided to jump straight to working with chess pieces. As I mentioned earlier, I want this arm to eventually play physical chess against me.<br><br>

            That said, I’m still brainstorming for a more dynamic task that could utilize voice commands, as chess isn’t the most effective way to showcase a speech-to-text model—it’s generally a pretty quiet game.<br><br>As always, I like to begin with the data, and this time it’s taking a significant amount of time, especially since I need to label the images.

            <br>My Raspberry Pi with the camera is already set up, so I just need a simple Python script to start taking pictures. I’ll start with the rook piece; the plan is to collect around 300 samples, with 80% from my own setup—my chessboard, environment, and lighting—and the rest sourced from the internet, if easily available.

            <br><br>It sounds pretty simple and straightforward, and it is. I’ll post a quick video of the setup below.<br><br>

            <div> <video controls> <source src="/camera-setup-na.mp4" type="video/mp4"> Your browser does not support the video tag. </video> </div>
            <br><br>The script simply prompts the user to press "Enter" to take a photo or "q" to exit.

            <br><br>I know the camera would be much more flexible with a longer ribbon cable. But, as I mentioned in a recent update, it was tough to even find this one, so let’s just say I tried! As a good procrastinator, I’ll revisit this issue when I eventually work on the robot’s physical build, which will definitely require a much longer cable.
            <br> Will I regret it? Sure. Am I still going to ignore it? Of course.

            <br><br>
            After taking about 70 pictures, I realized three things: my life kind of sucks, I still have 11 more pieces to go (since I actually need to track the color for it to play against me), and labeling all these photos is going to be a real pain. So, the plan is to split the folder 50/50 between each color—black and white in my case.

            Later, I'll label each photo as either white_rook or black_rook while keeping the image name neutral, like rook_{i}.

            <p>Nice! So now I have around 200 pictures of rooks. I tried to change the point of view as much as possible, with some rooks on the table, some on the board, and others with different pieces. About 25% of the images feature both rooks in a single shot, with varying heights, angles, lighting, and so on. I’m going to pause for now and focus on the model itself; after all, with such a small dataset, I can always integrate more pictures and retrain based on the results.</p>

            <p>I installed labelImg, which seems to be one of the best tools for this task, and I’ve labeled all the pictures. Unfortunately, I didn’t find any valuable datasets online. I admit I didn’t look too hard because I worry that too much environmental variation could negatively impact the model. I might be mistaken, but I plan to use data augmentation, so I hope my environment will be sufficient. If not, I’ll completely change the room and lighting and take many more pictures.</p>

            <p>So now we have our folder of labeled rook images ready to feed into our model. My idea is to test a model using just this one piece to understand how much variance we still need—too many pictures? Too few? Too static with the background? I want to determine the best environment for taking pictures before I commit to snapping 3,000 of them and potentially going off track.</p>

            <p>Now, here’s my question: Should I build a model that simply classifies whether it’s a rook and what color it is? Or should I go for a model that recognizes all 12 different pieces? My concern with the latter option is that the model might overfit, since it would be designed to classify 12 different classes but may only learn the features of the rook. On the other hand, the first model seems somewhat limited, as it would only classify whether a piece is a rook or not, leaving no room for the other pieces when I eventually add them. This means I’d likely need to rewrite the entire model, which defeats the purpose of starting with a simple classification.</p>

            <p>So, I’m at a crossroads where I need to think carefully about whether to gather all the data now and then build the model or to continue with the current approach. In the meantime, I’ve run out of free time, so I’ll use tonight to make a decision.</p>
            `,
            tag: "ai"
        },
        {
            title: "Update 9: More Object Detection with PyTorch",

            content: `Two days are passed. A night was not enough. It's funny because I did the wrong choice anyways (kinda), but that's the beauty, I guess. <br><br> I decided to go with a smaller model, focused only on the rook, just to understand what building one means. The majority of the resources I found online were using PyTorch, so I needed to learn it. Also, my tensorflow skills were not that much as I acquired the necessary just for the wake word model, which I will say it was much easier than this. <br><br> I found a very good video on YouTube, one day of content, for free. I watched the entire thing in a little more than a day and felt pretty confident already since it's just notation, if you already know the concept of machine and deep learning. You can find the video here: <a href="https://www.youtube.com/watch?v=V_xro1bcAuA&t=81442s" target="_blank"> PyTorch for Deep Learning & Machine Learning – Full Course</a>.<br> After this, I tried to build, as I said, a smaller model, which the only requirement was predicting if in the image there is a rook or not, and if so, if it's black or white. I went for a classic CNN architecture with two blocks (conv -> relu -> conv -> relu -> maxPool). After spending some hours and trying to do some testing I realized two things: the first one was that such an architecture is for binary classification more than multi-class classification, so it was more a model for rook/not rook, meaning no space for the color part; the second was that even though I were to slightly change the architecture to handle multi-class, my real goal is object detection, not a classification. So I was pretty wrong the entire time.<br><br> Here we are, this morning I decided to make a blueprint first, with all the requirements and start from zero. I also did some research about the loading images phase, with also some LLMs helps, in order to understand as much as possible, due to the variety of errors I encountered in the previous version.<br> So I dedicated the morning to build the load_images.py class where the images, both labeled and not, are being processed. In order to do this, I also needed the entire dataset of pictures so I took around 1500 of them. Same procedure as in the previous update. <br><br> I used the CustomDatasetClass from PyTorch that requires the three different functions: the __init__ one where everything is initialized and the images are processed, a __len__ one, that simply returns the length of all the images in the dataset, and the __getitem__ one where the code is executed by passing a sample from the dataset each time. I added another function to help me process the data, called "parse_xml", which takes an xml_file as an argument and extracts all the features from it, like the color of the piece, the name of the piece, and the bounding box coordinates.<br><br> After this, you just need a main.py where you call the different methods, create the dataset, and load it through the DataLoader module. Data augmentation is also suggested in this case; I used the transforms module, which let me also transform the images into tensors, which is suggested too in order to train the model later on.<br><br> You can find the code below for reference.<br><br>
            <div class="code-images">
                <img class="code-img" src="/load_images_1.png">
            <img class="code-img" src="/load_images_2.png">
            <p class="caption">As you can see, in the main function, there is a function called "collate_fn" that I needed to implement because I was getting an error related to different batch sizes. The issue occurred because my labels vary in size; some images have two labels due to both colors being present in the same picture, while others have just one.</p>
            <img class ="code-img" src="/main_py.png">
            </div>
            <p class="caption">
             The images are loaded correctly, and the labels look accurate. I can see a series of coordinates when a box is detected, and [-1, -1, -1, -1] when it’s not.
            <br><br>Regarding the model, I've outlined the architecture, and after some consideration, I think my choice will be a version similar to the Yolo v5n, also known as v5 nano.<br>I may further reduce the number of convolutional layers since the dataset size is manageable, and I also need to consider performance. I'm going to run the model on a Raspberry Pi, so the computational power is limited; a heavier architecture would not only risk overfitting but also use too much of the device's power.  </p>`
            , tag: "ai"
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
