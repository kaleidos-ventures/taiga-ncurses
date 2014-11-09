# -*- coding: utf-8 -*-

"""
taiga_ncurses.controllers.wiki
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from concurrent.futures import wait

from . import base


class ProjectWikiSubController(base.Controller):
    def __init__(self, view, executor, state_machine):
        self.view = view
        self.executor = executor
        self.state_machine = state_machine

        self.view.wiki_page.on_wiki_page_change = self.handle_wiki_page_change

    def load(self):
        self.state_machine.transition(self.state_machine.PROJECT_WIKI)

        self.view.notifier.info_msg("Fetching Wiki")

        wiki_pages_f = self.executor.wiki_pages(self.view.project)
        wiki_pages_f.add_done_callback(self.handle_wiki_pages)

        futures = (wiki_pages_f,)
        futures_completed_f = self.executor.pool.submit(lambda : wait(futures, 10))
        futures_completed_f.add_done_callback(self.when_wiki_pages_fetched)

    def handle_wiki_pages(self, future):
        self.wiki_pages = future.result()
        if self.wiki_pages is not None:
            if len(self.wiki_pages) > 0:
                self.view.wiki_page.populate(self.wiki_pages, self.wiki_pages[0])
            self.state_machine.refresh()

    def when_wiki_pages_fetched(self, future_with_results):
        done, not_done = future_with_results.result()
        if len(done) == 1:
            self.view.notifier.info_msg("Wiki pages fetched")
            self.state_machine.refresh()
        else:
            # TODO retry failed operations
            self.view.notifier.error_msg("Failed to fetch wiki data")

    def handle_wiki_page_change(self, combo, item, state, user_data=None):
        wiki_page = item.value
        self.view.wiki_page.populate(self.wiki_pages, wiki_page)

        self.view.notifier.info_msg("Change to wiki page: '{}'".format(wiki_page["slug"]))
