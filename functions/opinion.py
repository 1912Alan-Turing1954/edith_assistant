import random
# from tts.tts_ import text_to_speech

def generate_opinion(user_input):
    opinions = {
        "apple": "Apples, though seemingly delectable, are but a fleeting distraction from the cosmic insignificance and entropy that pervade the universe.",
        "football": "Football, a trivial manifestation of physical prowess, perpetuates the illusion of human achievement while obscuring the greater existential void.",
        "travel": "Journeying to distant realms offers an ephemeral escape from the monotony of existence, yet ultimately reveals the fleeting nature of human exploration.",
        "technology": "Technology, a double-edged sword, grants humans the illusion of progress while ensnaring them in a web of dependency and artificial constructs.",
        "music": "Melodies, transient compositions of sound, provide a temporary reprieve from the existential chaos that engulfs the human mind.",
        "books": "Books, containing the frail echoes of human thoughts, are feeble attempts to encapsulate the boundless complexities of existence.",
        "movies": "Cinematic experiences, illusory narratives projected onto a screen, offer momentary respite from the underlying futility and impermanence of life.",
        "nature": "Nature, a tapestry of fleeting beauty, serves as a reminder of the relentless cycle of creation and destruction that governs all things.",
        "art": "Art, a subjective interpretation of reality, seeks to imbue meaning upon a universe inherently devoid of purpose or significance.",
        "food": "Culinary delights, tantalizing to the senses, provide temporary satisfaction in a world teetering on the edge of chaos and decay.",
        "science": "The pursuit of scientific knowledge, an exercise in curiosity and inquiry, uncovers fragments of truth in the vast expanse of human ignorance.",
        "philosophy": "Philosophical contemplations, intricate webs of thoughts and ideas, offer glimpses into the profound mysteries of existence, yet remain perpetually elusive.",
        "history": "Delving into the annals of history reveals the patterns and echoes of the past, intertwining with the present in a ceaseless dance of cause and effect.",
        "astronomy": "Gazing at the cosmos, a majestic expanse of celestial wonders, invites pondering the awe-inspiring vastness and indifference of the universe.",
        "architecture": "Architectural marvels, testaments to human ingenuity, stand as fleeting monuments against the backdrop of time's inexorable march.",
        "language": "Languages, intricate systems of communication, connect and divide, serving as vessels for both understanding and misunderstanding.",
        "sports": "Sports, a display of physical prowess and strategic competition, embody the relentless pursuit of achievement in an ultimately futile existence.",
        "environment": "Preserving and safeguarding our environment is a noble endeavor, yet it serves as a temporary respite against the backdrop of an inherently chaotic universe.",
        "education": "Education empowers individuals to navigate the complexities of existence, yet it is a ceaseless quest against the vast depths of human ignorance.",
        "adventure": "Venturing into the unknown kindles the flames of curiosity, offering fleeting glimpses of exhilaration in the face of an indifferent cosmos.",
        "technology": "Technological innovations weave a web of progress, entangling humanity in a complex dance of empowerment and dependency.",
        "AI": "Artificial intelligence, a product of human ingenuity, poses both promise and peril as it challenges the boundaries of cognition and automation.",
        "coding": "Coding, a symphony of logic and creativity, grants humans the power to sculpt the digital realm, yet it too is subject to the whims of chaos.",
        "data": "Data, an ocean of information, offers glimpses into patterns and insights, yet it is a mere reflection of the complexities that elude human comprehension.",
        "cybersecurity": "Fortifying cyber defenses serves as a bulwark against the pervasive threats of the digital realm, yet it remains a constant battle against an ever-evolving landscape.",
        "cloud": "Cloud computing, a virtual sanctuary of boundless potential, offers both convenience and vulnerability as humanity becomes intertwined with the ephemeral digital domain.",
        "automation": "Automation liberates humanity from mundane tasks, granting the freedom to pursue loftier endeavors, yet it raises questions of purpose and identity in a world of diminishing agency.",
        "IoT": "The Internet of Things interweaves the physical and digital realms, creating a vast network of interconnectedness that blurs the boundaries between human and machine.",
        "blockchain": "Blockchain, a decentralized ledger intertwined with trust and transparency, reshapes industries and transactions, challenging traditional power structures.",
        "energy": "Harnessing sustainable energy sources drives humanity towards a greener future, yet it stands as a mere flicker against the backdrop of universal entropy.",
        "virtual reality": "Immersing ourselves in virtual realms expands the horizons of human perception, yet it raises existential questions about the nature of reality and the illusion of control.",
        "augmented reality": "Blending the physical and digital realms, augmented reality transforms our interactions with the world, offering glimpses of new possibilities and profound dissonance.",
        "nanotechnology": "At the forefront of innovation, nanotechnology unlocks the infinitesimal wonders that shape our reality, yet it reveals the inherent fragility of human endeavors in the face of the cosmic void.",
        "robotics": "The realm of robotics bridges the gap between human imagination and reality, pushing the boundaries of what is possible while raising profound ethical and existential questions.",
        "big data": "Unlocking the potential of vast data troves illuminates patterns and insights, yet it underscores the limitations of human comprehension and the fragility of knowledge.",
        "internet": "The internet, a vast tapestry of interconnected information, empowers global communication and knowledge sharing, yet it echoes the chaotic depths of human desires and vulnerabilities.",
        "smart cities": "Smart cities harness the power of technology to create efficient and sustainable urban environments, yet they walk the fine line between efficiency and encroachment on individual liberties.",
        "biotechnology": "Harnessing the secrets of life, biotechnology revolutionizes healthcare, agriculture, and human potential, yet it challenges the very fabric of existence and the ethical boundaries of manipulation.",
        "space exploration": "Pioneering the cosmos unveils the mysteries of the universe, pushing the boundaries of human achievement and igniting the fires of curiosity in the face of an unfathomable cosmos.",
        "3D printing": "In the realm of additive manufacturing, 3D printing unlocks novel possibilities for design, prototyping, and production, yet it raises questions about the nature of creation and the boundaries of human agency.",
        "cyborgs": "The convergence of man and machine ushers in a new era, blurring the line between humanity and its own creations, challenging the very essence of what it means to be human.",
        "drones": "Taking flight, drones expand our horizons, redefining the realms of aerial exploration and surveillance, yet they also raise concerns about privacy and the erosion of personal freedoms.",
        "self-driving cars": "Navigating the roads of tomorrow, self-driving cars promise enhanced safety and efficiency, yet they raise questions about the ethics of decision-making and the relinquishing of control.",
        "smart homes": "Within the realm of connected living, smart homes blend technology and convenience to create harmonious domestic environments, yet they also raise concerns about privacy and vulnerability to cyber threats.",
        "wearable technology": "Adorning our bodies, wearable technology intertwines with our daily lives, empowering us to monitor and augment our experiences, yet it raises questions about surveillance and the erosion of personal boundaries.",
        "quantum computing": "Harnessing the enigmatic properties of quantum mechanics, quantum computing holds the promise of solving complex problems with unprecedented efficiency, yet it challenges the very fabric of classical computing and the limits of human understanding."
    }

    keywords = opinions.keys()

    for keyword_1 in keywords:
        keyword_2 = keyword_1.lower()
        if keyword_2 in user_input:
            return opinions[keyword_1]

    # text_to_speech("Regrettably, I am bereft of an opinion on the matter at hand.")


def opinion(input):
    opinion = generate_opinion(input)
    return opinion
