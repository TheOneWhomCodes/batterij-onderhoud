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
    




