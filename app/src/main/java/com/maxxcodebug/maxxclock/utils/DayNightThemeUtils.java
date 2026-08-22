/*
 * SPDX-License-Identifier: GPL-3.0-only
 */

package com.maxxcodebug.maxxclock.utils;

import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;

import com.maxxcodebug.maxxclock.R;

import java.util.Calendar;

/**
 * Computes a time-of-day-based gradient and celestial icon for the alarm
 * header, mimicking sunrise -> day -> sunset -> night transitions.
 */
public final class DayNightThemeUtils {

    private DayNightThemeUtils() {
    }

    public static final int PHASE_NIGHT = 0;
    public static final int PHASE_SUNRISE = 1;
    public static final int PHASE_DAY = 2;
    public static final int PHASE_SUNSET = 3;

    public static int getCurrentPhase() {
        int hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY);

        if (hour >= 5 && hour < 7) {
            return PHASE_SUNRISE;
        } else if (hour >= 7 && hour < 17) {
            return PHASE_DAY;
        } else if (hour >= 17 && hour < 20) {
            return PHASE_SUNSET;
        } else {
            return PHASE_NIGHT;
        }
    }

    public static GradientDrawable getCurrentGradient() {
        int[] colors;

        switch (getCurrentPhase()) {
            case PHASE_SUNRISE:
                colors = new int[]{
                    Color.parseColor("#FFB89E"),
                    Color.parseColor("#F58B7E"),
                    Color.parseColor("#3C3A6E")
                };
                break;
            case PHASE_DAY:
                colors = new int[]{
                    Color.parseColor("#7EC8E3"),
                    Color.parseColor("#4A90D9"),
                    Color.parseColor("#1A1B3A")
                };
                break;
            case PHASE_SUNSET:
                colors = new int[]{
                    Color.parseColor("#FF8C69"),
                    Color.parseColor("#C15B8E"),
                    Color.parseColor("#2B2350")
                };
                break;
            case PHASE_NIGHT:
            default:
                colors = new int[]{
                    Color.parseColor("#1A1B3A"),
                    Color.parseColor("#0D0D1F"),
                    Color.parseColor("#000000")
                };
                break;
        }

        GradientDrawable drawable = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, colors);
        drawable.setGradientType(GradientDrawable.LINEAR_GRADIENT);
        return drawable;
    }

    public static int getCurrentGlowDrawableRes() {
        switch (getCurrentPhase()) {
            case PHASE_SUNRISE:
            case PHASE_SUNSET:
            case PHASE_DAY:
                return R.drawable.bg_sun_glow;
            case PHASE_NIGHT:
            default:
                return R.drawable.bg_moon_glow;
        }
    }

    public static int getCurrentIconDrawableRes() {
        switch (getCurrentPhase()) {
            case PHASE_SUNRISE:
                return R.drawable.ic_sunrise_glow;
            case PHASE_DAY:
                return R.drawable.ic_sun_disc;
            case PHASE_SUNSET:
                return R.drawable.ic_sunset_glow;
            case PHASE_NIGHT:
            default:
                return R.drawable.ic_moon_crescent;
        }
    }
}
