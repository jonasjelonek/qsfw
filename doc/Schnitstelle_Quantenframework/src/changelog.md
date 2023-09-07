# Changelog

<table><tbody>
<tr>
    <td>30.08.2023</td>
    <td>Initiale Version</td>
</tr>
<tr>
    <td>07.09.2023</td>
    <td>
        <ul>
            <li>
                Die Typspezifikation für den Parameter `angle` der Funktionen `phase` und `cphase` wurde korrigiert. Er akzeptiert nur
                numerische Ausdrücke über den Typ `float` statt wie bisher auch `str`. Numerische Ausdrücke (bspw. '2 * e') sind ohne
                Anführungszeichen anzugeben.
            </li>
            <li>
                Erlaubte Anfangszustände bei der Funktion `circuit` wurden angepasst. Es sind jetzt auch `+` und `-` erlaubt zur
                Angabe bereits überlagerter Zustände. `+` und `-` müssen ohne Anführungszeichen angegeben werden.
            </li>
            <li>Changelog hinzugefügt</li>
        </ul>
    </td>
</tr>
</tbody></table>