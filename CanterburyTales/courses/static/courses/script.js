//    AUDIENCE SLIDER FUNCTIONS

function getTitles(values, special_defs, defs) {
    if (values in special_defs) {
        $t = special_defs[values];
    } else if (values[0] == values[1]) {
        $t = defs[values[0]];
    } else {
        $t = defs[values[0]].concat(' through ', defs[values[1]]);
    }

    return $t;

};

function createAudienceSlider(item, breakpoints, initial = [18, 65], enabled = true) {
    return item.bootstrapSlider({
        range: true,
        ticks: breakpoints,
        lock_to_ticks: true,
        id: 'slider',
        value: initial,
        enabled: enabled,
    })
};







