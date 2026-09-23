/// <reference types="../../node_modules/.vue-global-types/vue_3.5_0_0_0.d.ts" />
import { ref, computed } from 'vue';
import { useImagingStore } from '../store/imaging';
const store = useImagingStore();
const rois = ref([
    { label: 'lesion1', center: [30, 28, 32], radius: 6, selected: true }
]);
const selectedCount = computed(() => rois.value.filter(r => r.selected).length);
function addROI() {
    // 默认标签自动避让已有名称，保证每个区域单独命名
    let n = rois.value.length + 1;
    while (rois.value.some(r => r.label === `roi-${n}`))
        n++;
    rois.value.push({ label: `roi-${n}`, center: [32, 32, 32], radius: 8, selected: true });
}
function removeROI(i) { rois.value.splice(i, 1); }
function analyze() {
    const chosen = rois.value.filter(r => r.selected)
        .map(({ label, center, radius }) => ({ label, center: [...center], radius }));
    store.analyzeROI(chosen);
}
debugger; /* PartiallyEnd: #3632/scriptSetup.vue */
const __VLS_ctx = {};
let __VLS_components;
let __VLS_directives;
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['summary']} */ ;
/** @type {__VLS_StyleScopedClasses['summary']} */ ;
/** @type {__VLS_StyleScopedClasses['result-table']} */ ;
/** @type {__VLS_StyleScopedClasses['result-table']} */ ;
/** @type {__VLS_StyleScopedClasses['result-table']} */ ;
// CSS variable injection 
// CSS variable injection end 
__VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
    ...{ class: "panel" },
});
__VLS_asFunctionalElement(__VLS_intrinsicElements.h4, __VLS_intrinsicElements.h4)({});
const __VLS_0 = {}.ElButton;
/** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
// @ts-ignore
const __VLS_1 = __VLS_asFunctionalComponent(__VLS_0, new __VLS_0({
    ...{ 'onClick': {} },
    size: "small",
    ...{ style: {} },
}));
const __VLS_2 = __VLS_1({
    ...{ 'onClick': {} },
    size: "small",
    ...{ style: {} },
}, ...__VLS_functionalComponentArgsRest(__VLS_1));
let __VLS_4;
let __VLS_5;
let __VLS_6;
const __VLS_7 = {
    onClick: (__VLS_ctx.addROI)
};
__VLS_3.slots.default;
var __VLS_3;
for (const [roi, i] of __VLS_getVForSourceType((__VLS_ctx.rois))) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        key: (i),
        ...{ class: "roi-config" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "roi-row" },
    });
    const __VLS_8 = {}.ElCheckbox;
    /** @type {[typeof __VLS_components.ElCheckbox, typeof __VLS_components.elCheckbox, ]} */ ;
    // @ts-ignore
    const __VLS_9 = __VLS_asFunctionalComponent(__VLS_8, new __VLS_8({
        modelValue: (roi.selected),
        size: "small",
    }));
    const __VLS_10 = __VLS_9({
        modelValue: (roi.selected),
        size: "small",
    }, ...__VLS_functionalComponentArgsRest(__VLS_9));
    const __VLS_12 = {}.ElInput;
    /** @type {[typeof __VLS_components.ElInput, typeof __VLS_components.elInput, ]} */ ;
    // @ts-ignore
    const __VLS_13 = __VLS_asFunctionalComponent(__VLS_12, new __VLS_12({
        modelValue: (roi.label),
        size: "small",
        placeholder: "标签",
        ...{ style: {} },
    }));
    const __VLS_14 = __VLS_13({
        modelValue: (roi.label),
        size: "small",
        placeholder: "标签",
        ...{ style: {} },
    }, ...__VLS_functionalComponentArgsRest(__VLS_13));
    const __VLS_16 = {}.ElInputNumber;
    /** @type {[typeof __VLS_components.ElInputNumber, typeof __VLS_components.elInputNumber, ]} */ ;
    // @ts-ignore
    const __VLS_17 = __VLS_asFunctionalComponent(__VLS_16, new __VLS_16({
        modelValue: (roi.center[0]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }));
    const __VLS_18 = __VLS_17({
        modelValue: (roi.center[0]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }, ...__VLS_functionalComponentArgsRest(__VLS_17));
    const __VLS_20 = {}.ElInputNumber;
    /** @type {[typeof __VLS_components.ElInputNumber, typeof __VLS_components.elInputNumber, ]} */ ;
    // @ts-ignore
    const __VLS_21 = __VLS_asFunctionalComponent(__VLS_20, new __VLS_20({
        modelValue: (roi.center[1]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }));
    const __VLS_22 = __VLS_21({
        modelValue: (roi.center[1]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }, ...__VLS_functionalComponentArgsRest(__VLS_21));
    const __VLS_24 = {}.ElInputNumber;
    /** @type {[typeof __VLS_components.ElInputNumber, typeof __VLS_components.elInputNumber, ]} */ ;
    // @ts-ignore
    const __VLS_25 = __VLS_asFunctionalComponent(__VLS_24, new __VLS_24({
        modelValue: (roi.center[2]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }));
    const __VLS_26 = __VLS_25({
        modelValue: (roi.center[2]),
        size: "small",
        min: (0),
        max: (63),
        ...{ style: {} },
        controlsPosition: "right",
    }, ...__VLS_functionalComponentArgsRest(__VLS_25));
    const __VLS_28 = {}.ElInputNumber;
    /** @type {[typeof __VLS_components.ElInputNumber, typeof __VLS_components.elInputNumber, ]} */ ;
    // @ts-ignore
    const __VLS_29 = __VLS_asFunctionalComponent(__VLS_28, new __VLS_28({
        modelValue: (roi.radius),
        size: "small",
        min: (2),
        max: (20),
        ...{ style: {} },
        controlsPosition: "right",
    }));
    const __VLS_30 = __VLS_29({
        modelValue: (roi.radius),
        size: "small",
        min: (2),
        max: (20),
        ...{ style: {} },
        controlsPosition: "right",
    }, ...__VLS_functionalComponentArgsRest(__VLS_29));
    const __VLS_32 = {}.ElButton;
    /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
    // @ts-ignore
    const __VLS_33 = __VLS_asFunctionalComponent(__VLS_32, new __VLS_32({
        ...{ 'onClick': {} },
        size: "small",
        type: "danger",
        circle: true,
    }));
    const __VLS_34 = __VLS_33({
        ...{ 'onClick': {} },
        size: "small",
        type: "danger",
        circle: true,
    }, ...__VLS_functionalComponentArgsRest(__VLS_33));
    let __VLS_36;
    let __VLS_37;
    let __VLS_38;
    const __VLS_39 = {
        onClick: (...[$event]) => {
            __VLS_ctx.removeROI(i);
        }
    };
    __VLS_35.slots.default;
    var __VLS_35;
}
const __VLS_40 = {}.ElButton;
/** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
// @ts-ignore
const __VLS_41 = __VLS_asFunctionalComponent(__VLS_40, new __VLS_40({
    ...{ 'onClick': {} },
    type: "success",
    size: "small",
    loading: (__VLS_ctx.store.loading),
    disabled: (!__VLS_ctx.selectedCount),
    ...{ style: {} },
}));
const __VLS_42 = __VLS_41({
    ...{ 'onClick': {} },
    type: "success",
    size: "small",
    loading: (__VLS_ctx.store.loading),
    disabled: (!__VLS_ctx.selectedCount),
    ...{ style: {} },
}, ...__VLS_functionalComponentArgsRest(__VLS_41));
let __VLS_44;
let __VLS_45;
let __VLS_46;
const __VLS_47 = {
    onClick: (__VLS_ctx.analyze)
};
__VLS_43.slots.default;
(__VLS_ctx.selectedCount);
var __VLS_43;
if (__VLS_ctx.store.roiResults.length) {
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "results" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: "results-head" },
    });
    if (__VLS_ctx.store.roiSummary) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            ...{ class: "summary" },
        });
        (__VLS_ctx.store.roiSummary.total);
        __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({
            ...{ class: "ok" },
        });
        (__VLS_ctx.store.roiSummary.succeeded);
        if (__VLS_ctx.store.roiSummary.failed) {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.b, __VLS_intrinsicElements.b)({
                ...{ class: "bad" },
            });
            (__VLS_ctx.store.roiSummary.failed);
        }
    }
    const __VLS_48 = {}.ElButton;
    /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
    // @ts-ignore
    const __VLS_49 = __VLS_asFunctionalComponent(__VLS_48, new __VLS_48({
        ...{ 'onClick': {} },
        size: "small",
        type: "danger",
        plain: true,
    }));
    const __VLS_50 = __VLS_49({
        ...{ 'onClick': {} },
        size: "small",
        type: "danger",
        plain: true,
    }, ...__VLS_functionalComponentArgsRest(__VLS_49));
    let __VLS_52;
    let __VLS_53;
    let __VLS_54;
    const __VLS_55 = {
        onClick: (...[$event]) => {
            if (!(__VLS_ctx.store.roiResults.length))
                return;
            __VLS_ctx.store.clearROIResults();
        }
    };
    __VLS_51.slots.default;
    var __VLS_51;
    __VLS_asFunctionalElement(__VLS_intrinsicElements.table, __VLS_intrinsicElements.table)({
        ...{ class: "result-table" },
    });
    __VLS_asFunctionalElement(__VLS_intrinsicElements.thead, __VLS_intrinsicElements.thead)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.tr, __VLS_intrinsicElements.tr)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.th, __VLS_intrinsicElements.th)({});
    __VLS_asFunctionalElement(__VLS_intrinsicElements.tbody, __VLS_intrinsicElements.tbody)({});
    for (const [r, i] of __VLS_getVForSourceType((__VLS_ctx.store.roiResults))) {
        __VLS_asFunctionalElement(__VLS_intrinsicElements.tr, __VLS_intrinsicElements.tr)({
            key: (i),
            ...{ class: ({ failed: r.status === 'error' }) },
        });
        if (r.status === 'ok') {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({
                ...{ class: "c-label" },
            });
            (r.label);
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
            (r.mean);
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
            (r.std);
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
            (r.voxelCount);
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
            (r.min);
            (r.max);
        }
        else {
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({
                ...{ class: "c-label" },
            });
            (r.label);
            __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({
                colspan: "4",
                ...{ class: "c-error" },
            });
            (r.error);
        }
        __VLS_asFunctionalElement(__VLS_intrinsicElements.td, __VLS_intrinsicElements.td)({});
        const __VLS_56 = {}.ElButton;
        /** @type {[typeof __VLS_components.ElButton, typeof __VLS_components.elButton, typeof __VLS_components.ElButton, typeof __VLS_components.elButton, ]} */ ;
        // @ts-ignore
        const __VLS_57 = __VLS_asFunctionalComponent(__VLS_56, new __VLS_56({
            ...{ 'onClick': {} },
            size: "small",
            type: "danger",
            link: true,
        }));
        const __VLS_58 = __VLS_57({
            ...{ 'onClick': {} },
            size: "small",
            type: "danger",
            link: true,
        }, ...__VLS_functionalComponentArgsRest(__VLS_57));
        let __VLS_60;
        let __VLS_61;
        let __VLS_62;
        const __VLS_63 = {
            onClick: (...[$event]) => {
                if (!(__VLS_ctx.store.roiResults.length))
                    return;
                __VLS_ctx.store.removeROIResult(i);
            }
        };
        __VLS_59.slots.default;
        var __VLS_59;
    }
}
/** @type {__VLS_StyleScopedClasses['panel']} */ ;
/** @type {__VLS_StyleScopedClasses['roi-config']} */ ;
/** @type {__VLS_StyleScopedClasses['roi-row']} */ ;
/** @type {__VLS_StyleScopedClasses['results']} */ ;
/** @type {__VLS_StyleScopedClasses['results-head']} */ ;
/** @type {__VLS_StyleScopedClasses['summary']} */ ;
/** @type {__VLS_StyleScopedClasses['ok']} */ ;
/** @type {__VLS_StyleScopedClasses['bad']} */ ;
/** @type {__VLS_StyleScopedClasses['result-table']} */ ;
/** @type {__VLS_StyleScopedClasses['c-label']} */ ;
/** @type {__VLS_StyleScopedClasses['c-label']} */ ;
/** @type {__VLS_StyleScopedClasses['c-error']} */ ;
var __VLS_dollars;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            store: store,
            rois: rois,
            selectedCount: selectedCount,
            addROI: addROI,
            removeROI: removeROI,
            analyze: analyze,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
