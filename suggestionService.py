from googletranspython import googletransfn


def suggestion_array_fun(chat_d):
    suggestion_array_list = []

    suggestion = dict(suggestionText="🗺️" + googletransfn(" Nearest branch", chat_d.CG_LANG_CODE), suggestionInput="Nearest branch")

    suggestion_array_list.append(suggestion)

    suggestion = dict(suggestionText="✍️ " + googletransfn("Report an issue", chat_d.CG_LANG_CODE), suggestionInput="Report an issue")
    suggestion_array_list.append(suggestion)

    suggestion = dict(suggestionText="🗣️ " + googletransfn("Change Language", chat_d.CG_LANG_CODE), suggestionInput="Change Language")
    suggestion_array_list.append(suggestion)

    suggestion = dict(suggestionText="💸" + googletransfn("Pay Gold Loan Interest", chat_d.CG_LANG_CODE), suggestionInput="Pay Gold Loan Interest")
    suggestion_array_list.append(suggestion)

    suggestion = dict(suggestionText="💰 " + googletransfn("Get gold loan details", chat_d.CG_LANG_CODE), suggestionInput="Pledge Details")
    suggestion_array_list.append(suggestion)

    # suggestion = dict(suggestionText="📞 " + googletransfn("Call Back", chat_d.CG_LANG_CODE), suggestionInput="Call Back")
    # suggestion_array_list.append(suggestion)


    

    return suggestion_array_list




def suggestion_array_fun2(chat_d):

    suggestion_array_list2 = []
    suggestion = dict(suggestionText="" + googletransfn("Gold Loan", chat_d.CG_LANG_CODE), suggestionInput="Apply gold loan")

    suggestion_array_list2.append(suggestion)

    suggestion = dict(suggestionText="" + googletransfn("Other Loans", chat_d.CG_LANG_CODE), suggestionInput="Other verticals enquiry")
    suggestion_array_list2.append(suggestion)


    return suggestion_array_list2

