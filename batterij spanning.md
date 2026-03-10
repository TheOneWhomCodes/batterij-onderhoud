# Batterij spanning berekenen!

We probeerden de formule te gebruiken die we kregen van [shotsky](shotsky.md).

Spijtig genoeg, waren we soms naast de echte waarde, met als max uitwijking 50 milivolt.

Hierdoor gaan we in plaats van die formule, lineaire interpolatie.

## werkwijze lineaire interpolatie

We moeten instellen dat we een kleine punt hebben en een grote punt.

Onze y-as kunnen we gebruiken voor onze batterij spanning, en onze x-as zal de uitgemeten adc waarde zijn.


**bijvoorbeeld:** Een punt van (0.723,6) en een punt van (3.238,14), en we meten met onze adc 1V


Hiermee hebben we 2 punten waarmee we tussen kunnen meten.

Met deze **formule:**

$$
y(x) = y1 + \frac{x-x1}{x2-x1} * (y2-y1)
$$

Als we die punten zouden invullen zouden we dit krijgen:

$$
y(1) = 6 + \frac{1-0.723}{3.238-0.723} * (14-6) = 6.865625 V
$$

In dit voorbeeld zou dit dan een schatting zijn van onze batterij spanning
    

## mogelijk probleem!

Zoals u weet gebruiken we adafruit voor het controleren van onze ads1115 chip.

Het kan zijn dat ik iets fout heb gedaan, waardoor er stroom nogsteeds door andere poorten kan gaan, tijdens het meten van voltage met mijn code.

Wanneer we meten vanaf poort A0, terwijl we andere poorten hebben geconnecteerd. Kan er zijn dat er afwijkingen gebeuren.

Onze kalibratie gaat van **6V** tot **14V**.

Wat er voorvalt terwijl we A0 uitlezen met:

- andere poorten geconnecteerd

<img width="1315" height="580" alt="image" src="https://github.com/user-attachments/assets/39434cec-5326-4ba5-8660-9afc1faabc11" />

- alleen A0 geconnecteerd

<img width="1253" height="501" alt="image" src="https://github.com/user-attachments/assets/aff8388f-dcc6-4ee2-9383-7fc3d71034df" />






