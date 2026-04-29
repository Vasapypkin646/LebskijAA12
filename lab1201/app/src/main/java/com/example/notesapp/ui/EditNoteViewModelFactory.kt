package com.example.notesapp.ui

import androidx.lifecycle.AbstractSavedStateViewModelFactory
import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.savedstate.SavedStateRegistryOwner
import com.example.notesapp.data.NoteRepository

class EditNoteViewModelFactory(
    owner: SavedStateRegistryOwner,
    private val repository: NoteRepository,
    private val noteId: Int
) : AbstractSavedStateViewModelFactory(owner, null) {

    override fun <T : ViewModel> create(
        key: String,
        modelClass: Class<T>,
        handle: SavedStateHandle
    ): T {
        if (modelClass.isAssignableFrom(EditNoteViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return EditNoteViewModel(repository, noteId, handle) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}