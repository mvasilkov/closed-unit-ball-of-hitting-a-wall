const M = 1e6
const G = 10
const R = 100
const F = 0.0169
const K = 200
const T = 0.02

function hypot(x: number, y: number) {
    return Math.sqrt(x * x + y * y)
}

function lerp(a: number, b: number, t: number) {
    return (1 - t) * a + t * b
}

function lerpAngle(a: number, b: number, t: number) {
    b -= a
    b %= Math.PI * 2
    if (b > Math.PI) {
        b -= Math.PI * 2
    }
    else if (b < -Math.PI) {
        b += Math.PI * 2
    }
    return a + b * t
}

function paintGround(c: CanvasRenderingContext2D) {
    c.beginPath()
    c.arc(0, 0, R - 20, 0, Math.PI * 2)
    c.lineWidth = 2
    c.strokeStyle = '#18FFFF'
    c.stroke()
}

function paintDangerZone(c: CanvasRenderingContext2D) {
    c.save()

    c.beginPath()
    c.arc(0, 0, K * 2, 0, Math.PI * 2)
    c.lineWidth = 2
    c.strokeStyle = '#F50057'
    c.setLineDash([10, 20])
    c.stroke()

    c.restore()
}
