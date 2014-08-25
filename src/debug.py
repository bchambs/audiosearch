def query(complete, failed, new, pending):
    print
    print "===================QUERY==================="
    for item in failed:
        print "FAILED: %s" %(str(item))

    for item in  pending:
        print "PENDING: %s" %(str(item))  

    for item in  new:
        print "NEW: %s" %(str(item))  

    if complete:
        print "AVAILABLE: "
        for key in complete.keys():
            print "   %s = {" %(key)
            for k, v in complete[key].items():
                try:
                    print _format_k_v(k, v)
                except TypeError:
                    print "   None"
                except AttributeError:
                    print "   ITS A LIST"
            print "   }"
    print


def _format_k_v(k, v):
    lead = "      %s" %(k)
    offset = ' ' * (9 - len(k))

    if k == "data":
        return lead + offset + ": LIST of len: " + str(len(v))
    else:
        return lead + offset + ": " + str(v)

