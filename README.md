## Bildeflytter

Flytter bilder fra ```source``` til ```destination```-path og organiserer alle matchende filer i mapper per år.

Programmet legger alle bilder med "taken date" i mappen til det året.
Dersom bildet ikke har dato satt, vil programmet heller bruke modifisert-dato på filen.
Som siste utvei legger den alle bilder i "Unknown_year"-mappe.

I prosessen leter programmet etter matchende bilder. Dersom programmet finner et bilde med samme filnavn vil den sjekke filens innhold. Filer håndteres på følgende måte;
- Samme filnavn og samme innhold: hopp over
- Samme filnavn, men ulikt innhold: legg på _x der x er første nummer som ikke eksisterer.