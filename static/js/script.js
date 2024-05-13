/* Index */
var setVanta = () => {
    if (window.VANTA) window.VANTA.NET({
        el: ".hero",  // Target the hero section
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 15.00,
        color: 0xff6347,
        backgroundColor: 0x808080 
        
    })
}
window.onload = setVanta;




