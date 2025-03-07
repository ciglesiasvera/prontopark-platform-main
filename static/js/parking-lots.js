var svgContainer = null;
var toolbar = null;
var panZoomController = null;
var fullScreenBtn = null;
var exitFullscreenBtn = null;
var resizeToolbarTimeoutId = null;
const minZoom = 1;
const maxZoom = 8;
var defaultFontSize = null;

window.onload = function () {
    if (!svgContainer) {
        console.error("#svgContainer no encontrado");
        return;
    }

    let previousTargetX = 0;
    let previousTargetY = 0;
    let previousZoomFactor = 1;
    let previousPanX = 0;
    let previousPanY = 0;

    let mobileEventsHandler = {
        haltEventListeners: ['touchstart', 'touchend', 'touchmove', 'touchleave', 'touchcancel'],
        init: function (options) {
            var instance = options.instance
                , initialScale = 1
                , pannedX = 0
                , pannedY = 0

            // Init Hammer library
            // Listen only for pointer and touch events
            this.hammer = Hammer(options.svgElement, {
                inputClass: Hammer.SUPPORT_POINTER_EVENTS ? Hammer.PointerEventInput : Hammer.TouchInput
            })

            // Enable pinch
            this.hammer.get('pinch').set({ enable: true })

            // Handle double tap
            this.hammer.on('doubletap', function (ev) {
                instance.zoomIn()
            })

            // Handle pan
            this.hammer.on('panstart panmove', function (ev) {
                // On pan start reset panned variables
                if (ev.type === 'panstart') {
                    pannedX = 0
                    pannedY = 0
                }

                // Pan only the difference
                instance.panBy({ x: ev.deltaX - pannedX, y: ev.deltaY - pannedY })
                pannedX = ev.deltaX
                pannedY = ev.deltaY
            })

            // Handle pinch
            this.hammer.on('pinchstart pinchmove', function (ev) {
                // On pinch start remember initial zoom
                if (ev.type === 'pinchstart') {
                    initialScale = instance.getZoom()
                    instance.zoomAtPoint(initialScale * ev.scale, { x: ev.center.x, y: ev.center.y })
                }

                instance.zoomAtPoint(initialScale * ev.scale, { x: ev.center.x, y: ev.center.y })
            })

            // Prevent moving the page on some devices when panning over SVG
            options.svgElement.addEventListener('touchmove', function (e) { e.preventDefault(); });
        }

        , destroy: function () {
            this.hammer.destroy()
        }
    }

    panZoomController = svgPanZoom(svgContainer, {
        viewportSelector: '#pan-zoom-viewport',
        minZoom: minZoom,
        maxZoom: maxZoom,
        zoomScaleSensitivity: 0.4,
        fit: true,
        center: true,
        customEventsHandler: mobileEventsHandler,
        controlIconsEnabled: false,
        dblClickZoomEnabled: false
    });

    window.resetView = function () {
        console.log('resetView');
        // logObject(panZoomController.getZoom(), "Zoom inicial");
        // logObject(panZoomController.getPan(), "Pan inicial");
        previousTargetX = 0;
        previousTargetY = 0;
        previousPanX = 0;
        previousPanY = 0;
        panZoomController.reset();
        // let currentPan = panZoomController.getPan();
        // let currentZoom = panZoomController.getZoom();
        // animatePanAndZoom(-currentPan.x, -currentPan.y, minZoom, 500, 500)
        // logObject(panZoomController.getZoom(), "Zoom final");
        // logObject(panZoomController.getPan(), "Pan final");
    }

    window.enterFullScreen = function () {
        const container = document.getElementById('container');
        if (container.requestFullscreen) {
            container.requestFullscreen();
        } else if (container.mozRequestFullScreen) {
            container.mozRequestFullScreen();
        } else if (container.webkitRequestFullscreen) {
            svgContainer.webkitRequestFullscreen();
        } else if (container.msRequestFullscreen) {
            container.msRequestFullscreen();
        }

        // panZoomController.fit();
        exitFullScreenBtn.disabled = false;
        fullScreenBtn.disabled = true;

        resizeAndLocateToolbar();
    }

    window.exitFullScreen = function () {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        fullScreenBtn.disabled = false;
        exitFullScreenBtn.disabled = true;

        resizeAndLocateToolbar();
    }

    // Experimetal
    window.centerView0 = function (selectedId, zoomFactor = 1) {
        const targetElement = document.getElementById(selectedId);
        if (!targetElement) return;

        var realZoom = panZoomController.getSizes().realZoom;

        let bbox = targetElement.getBoundingClientRect();

        let svgPoint = svgContainer.createSVGPoint();
        svgPoint.x = bbox.x + bbox.width * 0.5;
        svgPoint.y = bbox.y + bbox.height * 0.5;
        let svgCenter = svgPoint.matrixTransform(svgContainer.getScreenCTM().inverse());

        let svgWidth = svgContainer.clientWidth;
        let svgHeight = svgContainer.clientHeight;
        let svgWidth_2 = svgWidth * 0.5;
        let svgHeight_2 = svgHeight * 0.5;

        var targetX = svgCenter.x - (svgWidth_2 - previousTargetX);
        var targetY = svgCenter.y - (svgHeight_2 - previousTargetY);

        previousTargetX = targetX;
        previousTargetY = targetY;

        panZoomController.pan({
            x: -(svgCenter.x * realZoom) + (panZoomController.getSizes().width / 2),
            y: -(svgCenter.y * realZoom) + (panZoomController.getSizes().height / 2)
        });
        // panZoomController.pan({ x: -targetX, y: -targetY });
        // panZoomController.zoom(zoomFactor);
    }

    // Experimetal
    window.centerView1 = function (selectedId, zoomFactor = 1) {
        const targetElement = document.getElementById(selectedId);
        if (!targetElement) return;

        let bbox = targetElement.getBoundingClientRect();

        let svgPoint = svgContainer.createSVGPoint();
        svgPoint.x = bbox.x + bbox.width * 0.5;
        svgPoint.y = bbox.y + bbox.height * 0.5;
        let svgCenter = svgPoint.matrixTransform(svgContainer.getScreenCTM().inverse());

        let svgWidth = svgContainer.clientWidth;
        let svgHeight = svgContainer.clientHeight;
        let svgWidth_2 = svgWidth * 0.5;
        let svgHeight_2 = svgHeight * 0.5;

        var targetX = svgCenter.x - (svgWidth_2 - previousTargetX);
        var targetY = svgCenter.y - (svgHeight_2 - previousTargetY);

        previousTargetX = targetX;
        previousTargetY = targetY;

        panZoomController.pan({ x: -targetX, y: -targetY });
        panZoomController.zoom(zoomFactor);
    }

    window.centerView = function (selectedId) {
        const targetZoom = 4;
        const maxPanDuration = 2000;
        const maxZoomDuration = 2000;
        console.log("====> centerView : " + selectedId);
        // resetView();

        const targetElement = document.getElementById(selectedId);
        if (!targetElement) return;

        // Get current position and zoom
        let currentPan = panZoomController.getPan();
        let currentZoom = panZoomController.getZoom();
        let realZoom = panZoomController.getSizes().realZoom;
        // console.log("previousPanX: " + previousPanX + " | previousPanY: " + previousPanY);
        // logObject(currentPan, "getPan inicial");
        // console.log("currentZoom: " + currentZoom);


        // Get the bbox of the element after applying transformations
        let bbox = targetElement.getBoundingClientRect();//getBoundingClientRect();

        // Get the transformation matrix from SVG to the graphic window
        let svgPoint = svgContainer.createSVGPoint();

        // Convert the coordinates of the graphic window to the SVG coordinate system.
        svgPoint.x = bbox.x + bbox.width * 0.5; // X-center in coordinates of the graphic window
        svgPoint.y = bbox.y + bbox.height * 0.5; // Y-center in coordinates of the graphic window
        // console.log("svgPointX: " + svgPoint.x + " | svgPointY: " + svgPoint.y);

        // Transform coordinates to SVG coordinate system
        let svgCenter = svgPoint.matrixTransform(svgContainer.getScreenCTM().inverse());
        // console.log("svgCenterX: " + svgCenter.x + " | svgCenterY: " + svgCenter.y);

        // Get SVG dimensions in the coordinate system of the graphic window
        let svgWidth = svgContainer.clientWidth;
        let svgHeight = svgContainer.clientHeight;

        // Calculates the new coordinates to center the element, adjusting the panning to the current zoom
        let svgWidth_2 = svgWidth * 0.5;
        let svgHeight_2 = svgHeight * 0.5;
        // console.log("svgWidth: " + svgWidth + " | svgHeight: " + svgHeight);
        // console.log("svgWidth/2: " + svgWidth_2 + " | svgHeight/2: " + svgHeight_2);

        // console.log("previousTargetX: " + previousTargetX + " | previousTargetY: " + previousTargetY);
        var targetX = svgCenter.x - (svgWidth_2 - 0 * previousTargetX + 0 * currentPan.x + 0 * previousPanX);// / zoomFactor;
        var targetY = svgCenter.y - (svgHeight_2 - 0 * previousTargetY + 0 * currentPan.y + 0 * previousPanY);// / zoomFactor;
        // console.log("targetX: " + targetX + " | targetY: " + targetY);

        // Update previous target values for next call
        previousTargetX = targetX;
        previousTargetY = targetY;
        previousPanX = currentPan.x;
        previousPanY = currentPan.y;
        previousZoomFactor = targetZoom;

        animatePanAndZoom(targetX, targetY, targetZoom, maxPanDuration, maxZoomDuration, () => highlightRect(targetElement, 800));
    }

    function animatePanAndZoom(targetPanX, targetPanY, targetZoom, maxPanDuration, maxZoomDuration, onComplete = null) {
        return new Promise(resolve => {
            console.log("start animation");
            logObject(panZoomController.getZoom(), "Zoom inicial");
            logObject(panZoomController.getPan(), "Pan inicial");

            // Interpolate real panning duration:
            // panDuration = 0; norm(targetPan - currentPan) = 0
            // panDuration = maxPanDuration; norm(targetPan - currentPan) = norm((svgWidth, svgHeight))
            let currentPan = panZoomController.getPan();
            let panDistanceX = Math.abs(targetPanX - currentPan.x);
            let panDistanceY = Math.abs(targetPanY - currentPan.y);
            let svgWidth = svgContainer.clientWidth;
            let svgHeight = svgContainer.clientHeight;
            let panFactor = Math.sqrt((panDistanceX * panDistanceX + panDistanceY * panDistanceY) /
                (svgWidth * svgWidth + svgHeight * svgHeight));
            let panDuration = maxPanDuration * panFactor;

            // Calculates the real zoom duration:
            // zoomDuration = 0; norm(targetZoom - currentZoom) = 0
            // zoomDuration = maxZoomDuration; norm(targetZoom - currentZoom) = maxZoom - minZoom
            let currentZoom = panZoomController.getZoom();
            let zoomDifference = Math.abs(targetZoom - currentZoom);
            let zoomDuration = (zoomDifference === 0) ? 0 : maxZoomDuration * zoomDifference / (maxZoom - minZoom);

            if (onComplete) {
                setTimeout(() => {
                    onComplete();
                }, panDuration + zoomDuration);
            }

            function animatePanFrame(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = timestamp - startTime;

                // Calculates normalized progress (0 to 1)
                var t = Math.min(progress / panDuration, 1);

                // Interpola el paneo
                var newX = currentPan.x + (targetPanX - currentPan.x) * t;
                var newY = currentPan.y + (targetPanY - currentPan.y) * t;

                // Interpolate panning
                panZoomController.pan({ x: -newX, y: -newY });

                // If the panning animation is not finished, continue with
                if (progress < panDuration) {
                    requestAnimationFrame(animatePanFrame);
                } else {
                    // When the panning is finished, the zoom animation starts.
                    animateZoom();
                }
            }

            function animateZoom() {
                if (zoomDuration === 0) {
                    return;
                }
                startTime = null; // Reset the time for the zoom animation

                function animateZoomFrame(timestamp) {
                    if (!startTime) startTime = timestamp;
                    var progress = timestamp - startTime;

                    // Calculates normalized progress (0 to 1)
                    var t = Math.min(progress / zoomDuration, 1);

                    // Interpolate zoom
                    var newZoom = currentZoom + (targetZoom - currentZoom) * t;

                    // Apply zoom
                    panZoomController.zoom(newZoom);

                    // If the zoom animation is not finished, continue with
                    if (progress < zoomDuration) {
                        requestAnimationFrame(animateZoomFrame);
                    } else { // end animation
                        console.log("end animation");
                        logObject(panZoomController.getZoom(), "Zoom final");
                        logObject(panZoomController.getPan(), "Pan final");
                    }
                }
                // Start zoom animation
                requestAnimationFrame(animateZoomFrame);
            }
            // Starts the panning animation
            var startTime = null;
            requestAnimationFrame(animatePanFrame);
        });
    }

    document.addEventListener("click", clickOnRect, false);
};

window.onresize = function () {
    panZoomController.resize();
    panZoomController.fit();
    panZoomController.center();
    // TODO: Make adjustments to make centerView work after SVG resizing
}

function highlightRect(rect, duration = 400) {
    return new Promise(resolve => {
        let svg = rect.closest("svg");

        // Clones the rect and places it on top of all of them to prevent the highlighting 
        // of the original rect from being occluded by neighboring rects.
        let clone = document.createElementNS("http://www.w3.org/2000/svg", "rect");

        // Copy required attributes from the original rect
        clone.setAttribute("x", rect.getAttribute("x"));
        clone.setAttribute("y", rect.getAttribute("y"));
        clone.setAttribute("width", rect.getAttribute("width"));
        clone.setAttribute("height", rect.getAttribute("height"));

        clone.classList.add('highlighted');

        clone.setAttribute("data-tippy-content", "999");
        // Obtain the total transformation over rect
        let ctm = rect.getCTM();

        // Apply the transformation on the rect clone
        let initialTransform = `matrix(${ctm.a}, ${ctm.b}, ${ctm.c}, ${ctm.d}, ${ctm.e}, ${ctm.f})`;
        clone.setAttribute("transform", initialTransform);

        // Add rect clone over all elements
        svg.appendChild(clone);

        animateGlow(clone, duration, () => {
            svg.removeChild(clone); // Delete clone after animation
        });
    });
}

function animateGlow(rect, duration = 400, onComplete = null) {
    // duration : total duration in ms
    const maxGlow = 80; // Maximum glow size
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = (timestamp - startTime) / duration;
        if (progress > 1) progress = 1;

        let glowSize = progress < 0.5 ?
            maxGlow * (progress * 2) : // Grow
            maxGlow - maxGlow * ((progress - 0.5) * 2); // Decrease

        // Apply the glow effect using an SVG filter
        rect.setAttribute("filter", `url(#glowFilter)`);
        rect.setAttribute("stroke-width", glowSize / 10);

        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            rect.removeAttribute("filter");
            rect.removeAttribute("stroke-width"); // Restore border stroke
            if (onComplete) {
                onComplete();
            };
        }
    }

    requestAnimationFrame(step);
}

// Experimental. Produces glow animation to a rect by enlarging and then shrinking its size. 
// Currently works well only with unrotated rect
function highlightRectWithGrowth(rect, duration = 400) {

    let svg = rect.closest("svg");

    let clone = rect.cloneNode(true); // Clone the rect and copy its attributes
    clone.setAttribute("pointer-events", "none");

    // Get dimensions and center of rect in original coordinates
    let bbox = rect.getBBox();
    let cx = bbox.x + bbox.width / 2;
    let cy = bbox.y + bbox.height / 2;

    // Transform the center to global space using the total transformation
    let ctm = rect.getCTM();
    let transformedCx = ctm.e + ctm.a * cx + ctm.c * cy;
    let transformedCy = ctm.f + ctm.b * cx + ctm.d * cy;

    // Apply the initial transformation to the clone
    let initialTransform = `matrix(${ctm.a}, ${ctm.b}, ${ctm.c}, ${ctm.d}, ${ctm.e}, ${ctm.f})`;
    clone.setAttribute("transform", initialTransform);

    // Add clone over all elements
    svg.appendChild(clone);

    animateGrowth(clone, transformedCx, transformedCy, initialTransform, duration, () => {
        svg.removeChild(clone); // Delete clone after animation
    });
}

function animateGrowth(element, cx, cy, initialTransform, duration = 400, onComplete = null) {
    let maxScale = 3;
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        let progress = (timestamp - startTime) / duration;
        if (progress > 1) progress = 1;

        // Growth and reduction phase
        let scale = progress < 0.5 ?
            1 + (maxScale - 1) * (progress * 2) :
            maxScale - (maxScale - 1) * ((progress - 0.5) * 2);

        // Apply transformation while "maintaining" alignment
        element.setAttribute("transform", `
            ${initialTransform}
            translate(${cx}, ${cy})
            scale(${scale})
            translate(${-cx}, ${-cy})
        `);

        if (progress < 1) {
            requestAnimationFrame(step);
        } else if (onComplete) {
            onComplete();
        }
    }

    requestAnimationFrame(step);
}

document.addEventListener("DOMContentLoaded", function () {
    console.log('DOMContentLoaded')
    defaultFontSize = getDefaultFontSize();
    svgContainer = document.getElementById('svgContainer');
    fullScreenBtn = document.getElementById('fullscreenBtn');
    exitFullScreenBtn = document.getElementById('exitFullScreenBtn');
    loadParkingLots(svgContainer);

    // Inicializa Tippy.js en todos los elementos con data-tippy-content
    const tippyInstances = tippy('[data-tippy-content]', {
        placement: 'top', // Posición del tooltip
        arrow: true, // Muestra una flecha en el tooltip
        animation: 'scale', // Animación del tooltip
        theme: 'dark', // Tema del tooltip
        appendTo: () => document.fullscreenElement || document.body
    });

    // This is necessary because <foreignObject> toolbar in svg does not automatically adjust its size to the content it contains
    toolbar = document.getElementById('toolbar');
    resizeAndLocateToolbar();

    // // MutationObserver to detect changes in toolbar content ('controls') and to adjust toolbars
    // const contentObserver = new MutationObserver(debouncedResizeForeignObject);
    // contentObserver.observe(document.getElementById('controls'), {
    //     attributes: true,
    //     childList: true,
    //     subtree: true,
    //     characterData: true,
    // })

    // Observe changes in SVG attributes (height, x, y), to reposition toolbar, e.g. when toggling full screen
    const svgObserver = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            if (mutation.type === 'attributes' &&
                (mutation.attributeName === 'height' ||
                    mutation.attributeName === 'x' ||
                    mutation.attributeName === 'y')) {
                debouncedResizeAndLocateToolbar();
            }
        }
    });
    svgObserver.observe(svgContainer, {
        attributes: true,
    });

    // Observe changes in SVG size due to browser window or CSS changes
    if (window.ResizeObserver) {
        const resizeObserver = new ResizeObserver(debouncedResizeAndLocateToolbar);
        resizeObserver.observe(svgContainer);
    } else {
        console.warn('ResizeObserver no es compatible con este navegador.');
    }

    document.getElementById('parkingId').addEventListener('click', function () {
        this.focus();
    });
});

function clickOnRect(event) {
    if (event.target !== event.currentTarget) {
        const clickedId = event.target.id;
        let rect = document.getElementById(clickedId);
        if (rect && rect.tagName == 'rect') {
            document.getElementById('parkingId').value = clickedId;
            // let color = window.getComputedStyle(rect).fill;
            // rect.style.fill = 'white';
            // setTimeout(function () { rect.style.fill = color; }, 400);
            highlightRect(rect, 250);
        }
        event.stopPropagation();
    }
}

function parseTransform(transformString) {
    const transform = {
        rotate: 0,
        translateX: 0,
        translateY: 0
    };

    // Parse the transformation chain
    if (transformString) {
        const regexRotate = /rotate\((-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\)/;
        const regexTranslate = /translate\((-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\)/;

        const rotateMatch = transformString.match(regexRotate);
        if (rotateMatch) {
            transform.rotate = parseFloat(rotateMatch[1]);
        }

        const translateMatch = transformString.match(regexTranslate);
        if (translateMatch) {
            transform.translateX = parseFloat(translateMatch[1]);
            transform.translateY = parseFloat(translateMatch[2]);
        }
    }
    return transform;
}

function addTextLabelsToRects0(parkingLotsGroup) {
    // Adds horizontally aligned text to all rects, considering that all rectangles are built horizontally, before being rotated.
    if (!parkingLotsGroup) return;
    const nestedSvg = parkingLotsGroup.querySelector("svg");
    if (!nestedSvg) return;

    nestedSvg.querySelectorAll("g").forEach(group => {
        // For each rect group create a group for the respective texts
        const textGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        textGroup.setAttribute("class", "numberCaption");
        textGroup.setAttribute("paint-order", "stroke");

        // Get the transformation of the main group (if any)
        const groupTransform = parseTransform(group.getAttribute("transform"));

        // Apply the same transformation to the group of texts
        textGroup.setAttribute("transform", `rotate(${groupTransform.rotate}, ${groupTransform.translateX}, ${groupTransform.translateY})`);

        group.querySelectorAll("rect").forEach(rect => {
            const id = rect.id;
            if (!id) {
                console.error(`Rectángulo sin ID: ${rect}`);
                return;
            }

            // Get rectangle attributes
            const x = parseFloat(rect.getAttribute("x")) || 0;
            const y = parseFloat(rect.getAttribute("y")) || 0;
            const width = parseFloat(rect.getAttribute("width")) || 0;
            const height = parseFloat(rect.getAttribute("height")) || 0;

            // If the rect has its own translation, it is combined (it is assumed that there are only rotations in the groups)
            const rectTransform = parseTransform(rect.getAttribute("transform"));
            const finalX = x + groupTransform.translateX + rectTransform.translateX;
            const finalY = y + groupTransform.translateY + rectTransform.translateY;

            // Calculate the central position of the rectangle
            let centerX = finalX + width / 2;
            let centerY = finalY + height / 2;

            // Determine text orientation
            let textRotation;
            if (true) {
                textRotation = width >= height ? 0 : -90; // Horizontal if wider, vertical if taller
            } else {
                // If the rectangle is taller than wide, we try to rotate the text
                const isVertical = height > width;
                textRotation = isVertical ? -90 : 0;

                // If the rectangle was built vertically, we rotate the text
                if (textRotation !== 0) {
                    // Calculate the center correctly considering the rotated text
                    centerX = finalX + height / 2;
                    centerY = finalY + width / 2;
                }
            }

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", centerX);
            text.setAttribute("y", centerY);
            text.setAttribute("y", centerY);
            text.setAttribute("alignment-baseline", "central");
            text.textContent = id;

            // Apply rotation to each text if necessary
            if (textRotation !== 0) {
                text.setAttribute("transform", `rotate(${textRotation}, ${centerX}, ${centerY})`);
            }

            textGroup.appendChild(text); // Add text to the nested group
        });
        group.appendChild(textGroup); // Add the text group inside the main group
    });
}

function addTextLabelsToRects(parkingLotsGroup, rectCallback = null) {
    // Adds horizontally aligned text to all rects, considering that the rect are constructed horizontally
    // or vertically, and possibly have individual rotations
    if (!parkingLotsGroup) return;
    const nestedSvg = parkingLotsGroup.querySelector("svg");
    if (!nestedSvg) return;

    // Add a group at the end of the DOM, which will contain all the texts, to ensure that the texts are over all the rect.
    let mainTextGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    nestedSvg.appendChild(mainTextGroup);

    nestedSvg.querySelectorAll("g").forEach(group => {
        // For each rect group create a group for the respective texts
        const textGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        textGroup.setAttribute("class", "numberCaption");
        textGroup.setAttribute("paint-order", "stroke");

        if (groupTransf = group.getAttribute("transform")) {
            textGroup.setAttribute("transform", groupTransf);
        }

        // Get the transformation of the main group (if any)
        const groupTransform = group.getCTM();

        group.querySelectorAll("rect").forEach(rect => {
            const id = rect.id;
            if (!id) return;

            // Get rectangle attributes
            const x = parseFloat(rect.getAttribute("x")) || 0;
            const y = parseFloat(rect.getAttribute("y")) || 0;
            const width = parseFloat(rect.getAttribute("width")) || 0;
            const height = parseFloat(rect.getAttribute("height")) || 0;

            // Obtain the transformation matrix of the rectangle
            const rectTransform = rect.getCTM();

            // Combine the transformation matrix of the group and the one of the rectangle.
            const combinedTransform = groupTransform.multiply(rectTransform);

            // Calculate the transformed positions using the combined matrix
            const finalPosition = rect.getBBox();
            const centerX = finalPosition.x + finalPosition.width / 2;
            const centerY = finalPosition.y + finalPosition.height / 2;

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", centerX);
            text.setAttribute("y", centerY);
            text.setAttribute("alignment-baseline", "central");
            text.textContent = id;

            // If the rectangle is taller than wide, it is vertical, rotate the text.
            const isVertical = height > width;
            const textRotation = isVertical ? -90 : 0;

            // Apply rotation to text if necessary
            if (textRotation !== 0) {
                text.setAttribute("transform", `rotate(${textRotation}, ${centerX}, ${centerY})`);
            }

            textGroup.appendChild(text); // Add text to the nested group

            if (rectCallback) {
                rectCallback(rect);
            }
        });

        mainTextGroup.appendChild(textGroup); // Add the text group inside the last main group
    });
}

function addTextLabelsToRects2(parkingLotsGroup) {
    // Adds horizontally aligned text to all rects, considering that the rectangles are constructed horizontally or vertically and possibly have individual rotations
    if (!parkingLotsGroup) return;
    const nestedSvg = parkingLotsGroup.querySelector("svg");
    if (!nestedSvg) return;

    nestedSvg.querySelectorAll("g").forEach(group => {
        // Find the SVG nested inside #parkingLots.
        const textGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        textGroup.setAttribute("class", "numberCaption");
        textGroup.setAttribute("paint-order", "stroke");
        // Get the transformation of the main group (if any)
        const groupTransform = group.getCTM();

        group.querySelectorAll("rect").forEach(rect => {
            const id = rect.id;
            if (!id) return;

            // Get rectangle attributes
            const x = parseFloat(rect.getAttribute("x")) || 0;
            const y = parseFloat(rect.getAttribute("y")) || 0;
            const width = parseFloat(rect.getAttribute("width")) || 0;
            const height = parseFloat(rect.getAttribute("height")) || 0;

            // Obtain the transformation matrix of the rectangle
            const rectTransform = rect.getCTM();

            // Combine the transformation matrix of the group and the one of the rectangle.
            const combinedTransform = groupTransform.multiply(rectTransform);

            // Calculate the transformed positions using the combined matrix
            const finalPosition = rect.getBBox();
            const centerX = finalPosition.x + finalPosition.width / 2;
            const centerY = finalPosition.y + finalPosition.height / 2;

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", centerX);
            text.setAttribute("y", centerY);
            text.setAttribute("alignment-baseline", "central");
            text.textContent = id;

            // If the rectangle is taller than wide, it is vertical, rotate the text.
            const isVertical = height > width;
            const textRotation = isVertical ? -90 : 0;

            // Apply rotation to text if necessary
            if (textRotation !== 0) {
                text.setAttribute("transform", `rotate(${textRotation}, ${centerX}, ${centerY})`);
            }

            textGroup.appendChild(text);  // Add text to the nested group
        });

        group.appendChild(textGroup); // Add the text group inside the main group
    });

    console.log("Text labels added");
}

function loadParkingLots(svgContainer) {
    const svgUrl = document.getElementById('parking-lots-link').getAttribute('href');
    let container = document.getElementById('parkingLots');
    if (!container) {
        console.error('Grupo "#parkingLots" no encontrado en elemento SVG');
        return;
    }
    // Fetch the SVG file content asynchronously and parse it into a DOM node
    fetch(svgUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`No se pudo cargar el archivo ${svgUrl}`);
            }
            return response.text();
        })
        .then(svgContent => {
            // Convert SVG content to a DOM node
            const parser = new DOMParser();
            const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
            const svgNode = svgDoc.documentElement;

            container.appendChild(svgNode);
            console.log('parking-lots loaded');

            // Adds to a rect a callback for mouseenter event, which moves the rect to the end of the container group. 
            // This ensures that when the rect is hovered, its stroke will not be hidden by adjacent rect.
            function setRectOnMouseEnterCallback(rect) {
                rect.addEventListener('mouseenter', () => {
                    rect.parentNode.appendChild(rect);
                });
            }

            addTextLabelsToRects(container, setRectOnMouseEnterCallback);

            // Define the filter for glow animation in the SVG
            let svgNS = "http://www.w3.org/2000/svg";
            let glowFilter = document.createElementNS(svgNS, "filter");
            glowFilter.setAttribute("id", "glowFilter");
            // glowFilter.innerHTML = `
            //     <feGaussianBlur in="SourceAlpha" stdDeviation="18" result="blur"/> <!-- More blur -->
            //     <feFlood flood-color="cyan" result="glowColor"/> <!-- Glow color -->
            //     <feComposite in="glowColor" in2="blur" operator="in" result="coloredBlur"/> <!-- Apply color to blur -->
            //     <feMerge>
            //         <feMergeNode in="coloredBlur"/> <!-- First layer of glow -->
            //         <feMergeNode in="coloredBlur"/> <!-- Second layer of glow -->
            //         <feMergeNode in="coloredBlur"/> <!-- Third layer of glow -->
            //         <feMergeNode in="SourceGraphic"/> <!-- Original graphic -->
            //     </feMerge>
            // `;
            glowFilter.innerHTML = `
            <feMorphology in="SourceAlpha" operator="dilate" radius="3" result="thicken"/> <!-- Thickening the edge -->
            <feGaussianBlur in="thicken" stdDeviation="7" result="blur"/> <!-- Blur the edge -->
            <feFlood flood-color="cyan" result="glowColor"/> <!-- Border color -->
            <feComposite in="glowColor" in2="blur" operator="in" result="coloredBlur"/> <!-- Apply color to the border -->
            <feMerge>
                <feMergeNode in="coloredBlur"/> <!-- Outer edge -->
                <feMergeNode in="SourceGraphic"/> <!-- Original graphic -->
            </feMerge>
            `;
            svgContainer.appendChild(glowFilter);
        })
        .catch(error => {
            console.error(`Error al cargar archivo ${svgUrl} `, error);
        });
}

function resizeAndLocateToolbar() {
    return;
    const toolbar = document.getElementById('toolbar');
    const width = toolbar.clientWidth;
    const height = toolbar.clientHeight;
    let x = (svgContainer.clientWidth - width) * 0.5;
    let y = (svgContainer.clientHeight - height - emToPixels(0.3));
    toolbar.style.left = x + 'px';
    toolbar.style.top = y + 'px';
}

function debouncedResizeAndLocateToolbar() {
    clearTimeout(resizeToolbarTimeoutId);
    resizeToolbarTimeoutId = setTimeout(resizeAndLocateToolbar, 100);
}

function logObject(obj, objName = "object") {
    console.log(`${objName}: ${JSON.stringify(obj, null, 2)} `);
}

function getDefaultFontSize() {
    const tempDiv = document.createElement('div');
    tempDiv.style.cssText = 'position: absolute; visibility: hidden; height: 0px; width: 1000em';
    document.body.appendChild(tempDiv);
    const fontSizeInPixels = tempDiv.offsetWidth / 1000;
    document.body.removeChild(tempDiv);
    return fontSizeInPixels;
}

function emToPixels(em) {
    if (!defaultFontSize) {
        console.error("defaultFontSize debe inicializarse llamando a getDefaultFontSize()");
    }
    return Math.round(em * defaultFontSize);
}