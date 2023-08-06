from django.core.management.base import BaseCommand, CommandError, OutputWrapper
from django.core.management.color import color_style, no_style

from ..decorators import command_stat

class StatCommand(BaseCommand):

    def execute(self, *args, **options):
        """
        Try to execute this command, performing system checks if needed (as
        controlled by the ``requires_system_checks`` attribute, except if
        force-skipped).
        """
        if options['force_color'] and options['no_color']:
            raise CommandError("The --no-color and --force-color options can't be used together.")
        if options['force_color']:
            self.style = color_style(force_color=True)
        elif options['no_color']:
            self.style = no_style()
            self.stderr.style_func = None
        if options.get('stdout'):
            self.stdout = OutputWrapper(options['stdout'])
        if options.get('stderr'):
            self.stderr = OutputWrapper(options['stderr'])

        if self.requires_system_checks and not options['skip_checks']:
            self.check()
        if self.requires_migrations_checks:
            self.check_migrations()

        # output = self.handle(*args, **options)
        output = self._execute(*args, **options)
        if output:
            if self.output_transaction:
                connection = connections[options.get('database', DEFAULT_DB_ALIAS)]
                output = '%s\n%s\n%s' % (
                    self.style.SQL_KEYWORD(connection.ops.start_transaction_sql()),
                    output,
                    self.style.SQL_KEYWORD(connection.ops.end_transaction_sql()),
                )
            self.stdout.write(output)
        return output

    def _execute(self,*args,**options):
        return command_stat(self.handle)(self,*args,**options)

