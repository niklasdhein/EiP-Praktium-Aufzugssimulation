Unser Ziel
- einen "schlauen" Algorithmus finden
- Code so modular wie möglich halten

Features der Simulation
- Laden über config.json Datei
- Aufzüge sprechen sich dynamisch ab
- Ist auf dem Weg zum Ziel eine Person, dann wird diese mitgenommen
- Bunker- und Penthouseetagen, die nur von bestimmten Personen erreicht werden können
- Animierte Passagiere und Aufzüge
- Statistikdiagramme
- Komplette Simulation geschwindigkeits- und faktorbasiert. Also nicht fixe Simulationsteps pro Frame, sondern unabhängig von der Framerate

Anleitung zum Ausführen
- Mit Python main.py ausführen oder, wenn Modus gesetzt ist ./main.py - dabei ist es aber wichtig, dass virtuelle Environment wie in Zeile 1 in main.py unter .venv/ definiert ist, sonst wird der Interpreter nicht gefunden
- Andernfalls kann mit GUI.py mit Python gestartet werden, das die Simulation mit den dort eingegebenen Werten startet. Wichtig ist, dass vorher manuell in main.py korrekt gesetzt wird, ob die Simulation die Werte aus der Konfigurationsdatei (config.json) einliest oder die aus dem GUI übernimmt
- Zusätzlich lassen sich in der Konfigurationsdatei Simulationsparameter einstellen, zwei mehr als in der GUI, nämlich ob Sprites benutzt werden sollen oder ein Skalierungsfaktor

### NOTE
Das Repository existiert im Rahmen des zweiwöchigen Praktikums des Moduls "Einfühung in die Programmierung" der JGU Mainz aus dem Wintersemester 25/26. Ursprünglich war es als GitLab Repository angelegt.
