function checkValidation(e) {
    const bool = {}

    const chiocciola = () => {
        for (let i in e) {
            if (e[i] == ' ') {
                window.alert('non puoi inserire spazi nel campo email')
                e = ''
            }
            else if (e[i] == '@') {
                let bool1 = true
                return bool1
            }
        }



    }
    const fine = () => {
        if (e.slice(-4) == '.com' || e.slice(-4) == '.COM' || e.slice(-3) == '.it' || e.slice(-3) == '.IT' || e.slice(-4) == '.net' || e.slice(-4) == '.NET') {
            let bool2 = true
            return bool2
        }
    }


    bool['chiocciola'] = chiocciola()
    bool['validi'] = fine()
    if (bool['validi'] && bool['chiocciola']) {
        bool['email'] = e
    }

    return bool['email']

}











function ValidationPassword(e) {


    let pas = {}

    const minLength = () => {
        const A0 = () => {
            if (e.length >= 8) {
                let bool = true
                return bool
            }
            if (e.length <= 8) {
                window.alert('errore password premi ctrl + 5 per HelpPassword')
                e = ''
            }
        }
        return A0()
    }

    const caratteriSpeciali = () => {

        let pointValidation = []


        const A0 = () => {
            for (let i in e) {
                if (e[i] == '!') {
                    let bool = true
                    return bool
                }
                if (e[i] == ' ') {
                    window.alert('non puoi inserire spazi nel campo password')
                }
            }
        }
        const B0 = () => {
            for (let i in e) {
                if (e[i] == '|') {
                    let bool = true
                    return bool
                }
            }
        }
        const C0 = () => {
            for (let i in e) {
                if (e[i] == '£') {
                    let bool = true
                    return bool
                }
            }
        }
        const D0 = () => {
            for (let i in e) {
                if (e[i] == '$') {
                    let bool = true
                    return bool
                }
            }
        }
        const E0 = () => {
            for (let i in e) {
                if (e[i] == '%') {
                    let bool = true
                    return bool
                }
            }
        }
        const F0 = () => {
            for (let i in e) {
                if (e[i] == '&') {
                    let bool = true
                    return bool
                }
            }
        }
        const G0 = () => {
            for (let i in e) {
                if (e[i] == '?') {
                    let bool = true
                    return bool
                }
            }
        }

        const A1 = () => {
            for (let i in e) {
                if (e[i] == '^') {
                    let bool = true
                    return bool
                }
            }
        }
        const B1 = () => {
            for (let i in e) {
                if (e[i] == '*') {
                    let bool = true
                    return bool
                }
            }
        }
        const C1 = () => {
            for (let i in e) {
                if (e[i] == '+') {
                    let bool = true
                    return bool
                }
            }
        }
        const D1 = () => {
            for (let i in e) {
                if (e[i] == '-' || e[i] == '_') {
                    let bool = true
                    return bool
                }
            }
        }
        const E1 = () => {
            for (let i in e) {
                if (e[i] == '§') {
                    let bool = true
                    return bool
                }
            }
        }
        const F1 = () => {
            for (let i in e) {
                if (e[i] == 'ç') {
                    let bool = true
                    return bool
                }
            }
        }
        const G1 = () => {
            for (let i in e) {
                if (e[i] == '=') {
                    let bool = true
                    return bool
                }
            }
        }

        pointValidation.push(A0())
        pointValidation.push(B0())
        pointValidation.push(C0())
        pointValidation.push(D0())
        pointValidation.push(E0())
        pointValidation.push(F0())
        pointValidation.push(G0())

        pointValidation.push(A1())
        pointValidation.push(B1())
        pointValidation.push(C1())
        pointValidation.push(D1())
        pointValidation.push(E1())
        pointValidation.push(F1())
        pointValidation.push(G1())



        return pointValidation
    }

    const maiuscole = () => {
        function isLetterMaiuscola(v) {
            return typeof v === 'string' && v === v.toUpperCase();
        }
        for (let i in e) {
            l = e[i]
            if (isLetterMaiuscola(l) == true) {
                return true
            }
        }
    }

    pas['minLength'] = minLength()
    pas['caratteriSpeciali'] = caratteriSpeciali()
    pas['maiuscole'] = maiuscole()

    

    if (pas['minLength']  && pas['maiuscole']) {
        pas['password'] = e
    }
    return pas['password']

}