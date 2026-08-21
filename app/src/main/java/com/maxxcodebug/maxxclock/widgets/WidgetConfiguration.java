// SPDX-License-Identifier: GPL-3.0-only

package com.maxxcodebug.maxxclock.widgets;

import static com.maxxcodebug.maxxclock.utils.WidgetUtils.KEY_LAUNCHED_FROM_WIDGET;

import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.maxxcodebug.maxxclock.R;
import com.maxxcodebug.maxxclock.settings.AppWidgetAnalogSettingsFragment;
import com.maxxcodebug.maxxclock.settings.AppWidgetDigitalSettingsFragment;
import com.maxxcodebug.maxxclock.settings.AppWidgetNextAlarmSettingsFragment;
import com.maxxcodebug.maxxclock.settings.AppWidgetVerticalSettingsFragment;
import com.maxxcodebug.maxxclock.uicomponents.CollapsingToolbarBaseActivity;

/**
 * Class called when the user launches the widget configuration from the widget.
 */
public class WidgetConfiguration {

    public static class AnalogWidgetConfiguration extends CollapsingToolbarBaseActivity {

        @Override
        protected String getActivityTitle() {
            return getString(R.string.analog_widget);
        }

        @Override
        public void onCreate(final Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            showFragmentFromWidget(this, savedInstanceState, new AppWidgetAnalogSettingsFragment());
        }
    }

    public static class DigitalWidgetConfiguration extends CollapsingToolbarBaseActivity {

        @Override
        protected String getActivityTitle() {
            return getString(R.string.digital_widget);
        }

        @Override
        public void onCreate(final Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            showFragmentFromWidget(this, savedInstanceState, new AppWidgetDigitalSettingsFragment());
        }
    }

    public static class VerticalWidgetConfiguration extends CollapsingToolbarBaseActivity {

        @Override
        protected String getActivityTitle() {
            return getString(R.string.digital_widget);
        }

        @Override
        public void onCreate(final Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            showFragmentFromWidget(this, savedInstanceState, new AppWidgetVerticalSettingsFragment());
        }
    }

    public static class NextAlarmWidgetConfiguration extends CollapsingToolbarBaseActivity {

        @Override
        protected String getActivityTitle() {
            return getString(R.string.digital_widget);
        }

        @Override
        public void onCreate(final Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            showFragmentFromWidget(this, savedInstanceState, new AppWidgetNextAlarmSettingsFragment());
        }
    }

    public static void showFragmentFromWidget(AppCompatActivity activity, Bundle savedInstanceState, Fragment fragment) {
        if (savedInstanceState == null) {
            Bundle args = fragment.getArguments();
            if (args == null) {
                args = new Bundle();
            }
            args.putBoolean(KEY_LAUNCHED_FROM_WIDGET, true);
            fragment.setArguments(args);

            activity.getSupportFragmentManager().beginTransaction()
                .replace(R.id.content_frame, fragment)
                .disallowAddToBackStack()
                .commit();
        }
    }

}
