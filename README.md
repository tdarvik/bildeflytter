## Bildeflytter

Flytter bilder fra ```source``` til ```destination```-path og organiserer alle matchende filer i mapper per år.

Kjør programmet med Python:

`./python bildeflytter.py "C:/bildemappe" "C:/album"` 

Behandler filer med følgende extensions:

`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`, `.webp`,`.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mkv`, `.m4v`, `.raw`, `.arw`, `.cr2`, `.cr3`, `.dng`, `.nef`, `.nrw`, `.orf`, `.raf`, `.rw2`, `.pef`, `.srw`, `.x3f`

Programmet legger alle bilder med "taken date" i mappen til det året, f.eks. `2024`.
Dersom bildet ikke har dato satt, vil programmet heller bruke modifisert-dato på filen for å finne årstallet.
Som siste utvei legger den alle bilder i `Unknown_year`-mappe.

I prosessen leter programmet etter matchende bilder. Dersom programmet finner et bilde med samme filnavn vil den sjekke filens innhold. Filer håndteres på følgende måte;
- Samme filnavn og samme innhold: hopp over
- Samme filnavn, men ulikt innhold: legg på `_x` der `x` er første nummer som ikke eksisterer.