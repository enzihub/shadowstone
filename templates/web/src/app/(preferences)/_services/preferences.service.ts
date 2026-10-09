// preferences.service.ts

'use server';

import { eq } from 'drizzle-orm';
import { db } from '@/db/db';
import { SelectUserPref, userPrefs, InsertUserPref } from '@/db/schema';
import { getOrCreateUser } from '@/app/(user)/_services/user.service';
export async function createUserPref(
  email: string,
  phone: string,
  timezone: string,
): Promise<SelectUserPref> {
  try {
    // First, ensure we have a user with a proper UUID
    const user = await getOrCreateUser(email);

    // Check if preference exists
    const existingPref = await db
      .select()
      .from(userPrefs)
      .where(eq(userPrefs.email, user.email))
      .limit(1);

    if (existingPref.length > 0) {
      return existingPref[0];
    }

    // Create new preference
    const newPref = await db
      .insert(userPrefs)
      .values({
        userId: user.id,
        email,
        timezone,
        phone,
        createdAt: new Date(),
        updatedAt: new Date(),
      } satisfies InsertUserPref)
      .returning();

    return newPref[0];
  } catch (error) {
    throw new Error(
      `Failed to create user preference: ${error instanceof Error ? error.message : 'Unknown error'}`,
    );
  }
}

export async function getUserPref(
  email: string,
): Promise<SelectUserPref | null> {
  try {
    const pref = await db
      .select()
      .from(userPrefs)
      .where(eq(userPrefs.email, email))
      .limit(1);

    return pref[0] || null;
  } catch (error) {
    return null;
  }
}

export async function upsertUserPref(
  userId: string,
  email: string,
  phone: string,
  description: string,
  timezone: string,
): Promise<SelectUserPref> {
  try {
    const existingPref = await db
      .select()
      .from(userPrefs)
      .where(eq(userPrefs.email, email))
      .limit(1);

    if (existingPref.length > 0) {
      // Update existing preference
      const updatedPref = await db
        .update(userPrefs)
        .set({
          phone,
          description,
          timezone,
          updatedAt: new Date(),
        })
        .where(eq(userPrefs.email, email))
        .returning();

      return updatedPref[0];
    } else {
      // Create new preference, linked to the users row for this email
      const user = await getOrCreateUser(email);
      const newPref = await db
        .insert(userPrefs)
        .values({
          userId: user.id,
          email,
          timezone,
          phone,
          description,
          createdAt: new Date(),
          updatedAt: new Date(),
        } satisfies InsertUserPref)
        .returning();

      return newPref[0];
    }
  } catch (error) {
    throw new Error(
      `Failed to upsert user preference: ${error instanceof Error ? error.message : 'Unknown error'}`,
    );
  }
}

