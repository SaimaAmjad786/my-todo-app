"use client";

import { useEffect, useRef } from "react";
import type { Todo } from "@/types/api";
import { scheduleNotification, requestNotificationPermission } from "@/lib/notifications";

export function useReminders(todos: Todo[] | undefined) {
  const scheduledReminders = useRef<Map<string, NodeJS.Timeout>>(new Map());

  useEffect(() => {
    if (!todos) return;

    // Request permission on first reminder-enabled todo
    const hasReminders = todos.some((todo) => todo.reminder_time && !todo.completed);
    if (hasReminders) {
      requestNotificationPermission();
    }

    // Clear old reminders
    scheduledReminders.current.forEach((timeout, id) => {
      if (!todos.find((t) => t.id === id)) {
        clearTimeout(timeout);
        scheduledReminders.current.delete(id);
      }
    });

    // Schedule new reminders
    todos.forEach((todo) => {
      if (todo.reminder_time && !todo.completed) {
        const existingTimeout = scheduledReminders.current.get(todo.id);
        if (existingTimeout) {
          clearTimeout(existingTimeout);
        }

        const reminderDate = new Date(todo.reminder_time);
        const timeout = scheduleNotification(
          `Reminder: ${todo.title}`,
          todo.description || "You have a task due soon!",
          reminderDate
        );

        if (timeout) {
          scheduledReminders.current.set(todo.id, timeout);
        }
      }
    });

    return () => {
      scheduledReminders.current.forEach((timeout) => clearTimeout(timeout));
      scheduledReminders.current.clear();
    };
  }, [todos]);
}
